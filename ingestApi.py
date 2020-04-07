from flask import Blueprint, render_template
import epicsModel, issuesModel, projectEpicsAndTicketsModel as peatm, epicsIssuesModel, ticketsModel, boardsModel

ingest_api_routes = Blueprint('ingest_api_routes', __name__)


@ingest_api_routes.route('/api/ingest/all')
def api_ingest_all():
    all_boards = boardsModel.get_boards()["boards"]
    for board in all_boards:
        print("Ingesting for board: %s" %(board["boardName"]))
        api_ingest_epics(board["boardName"])
        print("Finished ingesting epics")
        api_ingest_epics_issues(board["boardName"])
        print("Finished ingesting issues that belongs to the epics")
        api_ingest_issues(board["boardName"])
        print("Finished ingesting issues that does not belong to the epics")
    return "done!"

@ingest_api_routes.route('/api/ingest/epics/<board_name>')
def api_ingest_epics(board_name):
    repoId = boardsModel.get_repo_id(board_name)
    all_epics = epicsModel.fetch_epics(repoId)
    epic_issues = all_epics['epic_issues']

    epicsModel.delete_all_epics_for_board(board_name)

    for epic_issue in epic_issues:
        epic_issue_number = epic_issue['issue_number']
        epic_issue_details = issuesModel.fetch_issue(epic_issue_number, board_name)
        issue_status = issuesModel.issue_status(epic_issue_details)
        if issue_status is "epic":
            if epic_issue_details["state"] != "closed":
                epicsModel.insert_epics(epic_issue_number, epic_issue_details['title'], board_name)
        else:
            print("Issue status: %s" %(issue_status))
    return "epics ingestion is complete"


@ingest_api_routes.route('/api/ingest/test')
def api_test():
    ticket_issue = {"boardName": "ott-web-europe", "issueNumber": 1, "totalComments": 2}
    # ticketsModel.insert_or_update_ticket_comment_count(ticket_issue)
    return "do"

@ingest_api_routes.route('/api/ingest/epicsIssues/<board_name>')
def api_ingest_epics_issues(board_name):
    all_epics = epicsModel.get_epic_by_board_name(board_name)
    epicsIssuesModel.delete_all_epics_issues_for_board(board_name)
    issuesModel.delete_all_issues_for_board(board_name)
    repoId = boardsModel.get_repo_id(board_name)

    for epic in all_epics["epics"]:
        print("Attempting to fetch issues for epic: %s" %(epic["epicId"]))
        epic_issues = epicsIssuesModel.fetch_epic_issues(epic["epicId"], repoId)
        if "issues" in epic_issues:
            if epic_issues["issues"] == []:
                print(">>>> This epic has no issue!")
            for issue in epic_issues["issues"]:
                issue_number = issue["issue_number"]
                issue_status = issuesModel.fetch_issue_status(issue_number, repoId)

                if issue_status is not "epic":
                    epicsIssuesModel.insert_epics_issues(epic["epicId"], issue_number, board_name)
                    issue_does_not_exists = issuesModel.check_issue_exists(issue_number, board_name)
                    if issue_does_not_exists:
                        issue_details = issuesModel.fetch_issue(issue_number, board_name)
                        issuesModel.insert_issues(issue_number, board_name, issue_details["title"], issue_status, issue_details["html_url"])
                        # insert into the tickets too if it doesnt exists otherwise update it
                        ticket_issue = {"boardName": board_name, "issueNumber": issue_number, "totalComments": issue_details["comments"]}
                        ticketsModel.insert_or_update_ticket_comment_count(ticket_issue)
        else:
            print("ERROR: could not find any issue for %s" %(epic["epicId"]))
    return "epics issues ingestion complete"

@ingest_api_routes.route('/api/ingest/issues/<board_name>')
def api_ingest_issues(board_name):
    # this is to ingest those individual issues and are not part of an epic
    # It can be found in the projectEpicsAndTickets table where type issue
    repoId = boardsModel.get_repo_id(board_name)
    all_issues = peatm.get_all_issues_from_project(board_name)
    for issue in all_issues:
        issue_number = issue[2]
        issue_does_not_exists = issuesModel.check_issue_exists(issue_number, board_name)
        if issue_does_not_exists:
            issue_status = issuesModel.fetch_issue_status(issue_number, repoId)

            if issue_status is not "epic":
                issue_details = issuesModel.fetch_issue(issue_number, board_name)
                issuesModel.insert_issues(issue_number, board_name, issue_details['title'], issue_status, issue_details["html_url"])

    return 'ingested issues without Epic individually'
    # VUK010960
    # 07776824548
