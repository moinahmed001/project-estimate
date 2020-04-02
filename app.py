from flask import Flask, escape, request
import db
import epics, issues, projectEpicsAndTickets as peat
from flask import jsonify


app = Flask(__name__)
app.config.from_pyfile('config.cfg')

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/api/epics')
def api_epics():
    return jsonify(epics.get_epics())

@app.route('/api/issue/<board_name>/<issue_number>')
def api_issue(board_name, issue_number):
    return issues.get_issue(board_name, issue_number)

@app.route('/api/ingest/epics')
def api_ingest_epics():
    all_epics = epics.fetch_epics()
    epic_issues = all_epics['epic_issues']

    delete_epics_query = "DELETE FROM epics where boardName = '%s'" %(app.config['REPOS'])
    db.with_query(delete_epics_query)

    for epic_issue in epic_issues:
        epic_issue_number = epic_issue['issue_number']
        epic_issue_details = issues.fetch_issue(epic_issue_number)
        db.insert_epics(epic_issue_number, epic_issue_details['title'], app.config['REPOS'])

    return "epics ingestion is complete"


@app.route('/api/ingest/epicsIssues')
def api_ingest_epics_issues():
    all_epics = epics.get_epics()
    delete_epicsIssues_query = "DELETE FROM epicsIssues where boardName = '%s'" %(app.config['REPOS'])
    db.with_query(delete_epicsIssues_query)
    delete_issues_query = "DELETE FROM issues where boardName = '%s'" %(app.config['REPOS'])
    db.with_query(delete_issues_query)

    for epic in all_epics["epics"]:
        epic_issues = epics.fetch_epic_issues(epic["epicId"])
        for issue in epic_issues["issues"]:
            issue_number = issue["issue_number"]
            db.insert_epics_issues(epic["epicId"], issue_number, app.config['REPOS'])
            issue_does_not_exists = issues.check_issue_exists(issue_number, app.config['REPOS'])
            if issue_does_not_exists:
                issue_status = issues.fetch_issue_status(issue_number)
                if issue_status is not "epic":
                    issue_details = issues.fetch_issue(issue_number)
                    db.insert_issues(issue_number, app.config['REPOS'], issue_details['title'], issue_status, issue_details["html_url"])
    return "epics issues ingestion complete"

@app.route('/api/ingest/issues')
def api_ingest_issues():
    # this is to ingest those individual issues and are not part of an epic
    # It can be found in the projectEpicsAndTickets table where type issue
    all_issues = peat.get_all_issues_from_project(app.config['REPOS'])
    print(all_issues)
    for issue in all_issues:
        issue_number = issue[2]
        issue_status = issues.fetch_issue_status(issue_number)
        if issue_status is not "epic":
            issue_details = issues.fetch_issue(issue_number)
            db.insert_issues(issue_number, app.config['REPOS'], issue_details['title'], issue_status, issue_details["html_url"])

    return 'done'
    # VUK010960
    # 07776824548
