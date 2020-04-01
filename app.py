from flask import Flask, escape, request
import db
import epics, issues
from flask import jsonify


app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/api/epics')
def api_epics():
    return jsonify(epics.get_epics())

@app.route('/api/issue/<issue_number>')
def api_issue(issue_number):
    return issues.get_issue(issue_number)

@app.route('/api/ingest/epics')
def api_ingest_epics():
    all_epics = epics.fetch_epics()

    epic_issues = all_epics['epic_issues']
    db.truncate_table('epics')
    for epic_issue in epic_issues:
        epic_issue_number = epic_issue['issue_number']
        epic_issue_details = issues.fetch_issue(epic_issue_number)
        db.insert_epics(epic_issue_number, epic_issue_details['title'])

    return "epics ingestion is complete"


@app.route('/api/ingest/epicsIssues')
def api_ingest_epics_issues():
    all_epics = epics.get_epics()
    db.truncate_table('epicsIssues')
    for epic in all_epics["epics"]:
        epic_issues = epics.fetch_epic_issues(epic["epicId"])
        for issue in epic_issues["issues"]:
            db.insert_epics_issues(epic["epicId"], issue["issue_number"])

    return "epics issues ingestion complete"

@app.route('/api/ingest/issues')
def api_ingest_issues():
    return 'done'
