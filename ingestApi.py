from flask import Blueprint, render_template
import epicsModel, issuesModel, projectEpicsAndTicketsModel as peatm, epicsIssuesModel, ticketsModel

ingest_api_routes = Blueprint('ingest_api_routes', __name__)


@ingest_api_routes.route('/api/ingest/all')
def api_ingest_all():
    api_ingest_epics()
    api_ingest_epics_issues()
    api_ingest_issues()
    return "done!"

@ingest_api_routes.route('/api/ingest/epics')
def api_ingest_epics():
    all_epics = epicsModel.fetch_epics()
    epic_issues = all_epics['epic_issues']

    epicsModel.delete_all_epics_for_board()

    for epic_issue in epic_issues:
        epic_issue_number = epic_issue['issue_number']
        epic_issue_details = issuesModel.fetch_issue(epic_issue_number)
        if epic_issue_details["state"] != "closed":
            epicsModel.insert_epics(epic_issue_number, epic_issue_details['title'], "ott-web-europe")

    return "epics ingestion is complete"


@ingest_api_routes.route('/api/ingest/test')
def api_test():
    ticket_issue = {"boardName": "ott-web-europe", "issueNumber": 1, "totalComments": 2}
    ticketsModel.insert_or_update_ticket(ticket_issue)
    return "do"

@ingest_api_routes.route('/api/ingest/epicsIssues')
def api_ingest_epics_issues():
    all_epics = epicsModel.get_epics()
    epicsIssuesModel.delete_all_epics_issues_for_board()
    issuesModel.delete_all_issues_for_board()

    for epic in all_epics["epics"]:
        epic_issues = epicsIssuesModel.fetch_epic_issues(epic["epicId"])
        for issue in epic_issues["issues"]:
            issue_number = issue["issue_number"]
            issue_status = issuesModel.fetch_issue_status(issue_number)
            if issue_status is not "epic":
                epicsIssuesModel.insert_epics_issues(epic["epicId"], issue_number, "ott-web-europe")
                issue_does_not_exists = issuesModel.check_issue_exists(issue_number, "ott-web-europe")
                if issue_does_not_exists:
                    issue_details = issuesModel.fetch_issue(issue_number)
                    issuesModel.insert_issues(issue_number, "ott-web-europe", issue_details["title"], issue_status, issue_details["html_url"])
                    # insert into the tickets too if it doesnt exists otherwise update it
                    ticket_issue = {"boardName": "ott-web-europe", "issueNumber": issue_number, "totalComments": issue_details["comments"]}
                    ticketsModel.insert_or_update_ticket(ticket_issue)
    return "epics issues ingestion complete"

@ingest_api_routes.route('/api/ingest/issues')
def api_ingest_issues():
    # this is to ingest those individual issues and are not part of an epic
    # It can be found in the projectEpicsAndTickets table where type issue
    all_issues = peatm.get_all_issues_from_project("ott-web-europe")
    for issue in all_issues:
        issue_number = issue[2]
        issue_does_not_exists = issuesModel.check_issue_exists(issue_number, "ott-web-europe")
        if issue_does_not_exists:
            issue_status = issuesModel.fetch_issue_status(issue_number)

            if issue_status is not "epic":
                issue_details = issuesModel.fetch_issue(issue_number)
                issuesModel.insert_issues(issue_number, "ott-web-europe", issue_details['title'], issue_status, issue_details["html_url"])

    return 'ingested issues without Epic individually'
    # VUK010960
    # 07776824548
