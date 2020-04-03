from flask import Flask, escape, request, Blueprint
from views import views_routes
import epicsModel, issuesModel, projectEpicsAndTicketsModel as peatm, projectsModel, epicsIssuesModel, ticketsModel
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(views_routes)
app.config.from_pyfile('config.cfg')

@app.route('/')
def hello():
    routes = []
    for route in app.url_map.iter_rules():
        routes.append('{url: %s}' % route)
    return jsonify(routes)

@app.route('/api/epics')
def api_epics():
    return jsonify(epicsModel.get_epics())

@app.route('/api/issues')
def api_issues():
    return jsonify(issuesModel.get_issues())

@app.route('/api/epicsIssues')
def api_epics_issues():
    return jsonify(epicsIssuesModel.get_epics_issues())

@app.route('/api/projects')
def api_projects():
    return jsonify(projectsModel.get_projects())

@app.route('/api/tickets')
def api_tickets():
    return jsonify(ticketsModel.get_tickets())

@app.route('/api/issue/<board_name>/<issue_number>')
def api_issue(board_name, issue_number):
    return issuesModel.get_issue(board_name, issue_number)


@app.route('/api/ingest/all')
def api_ingest_all():
    api_ingest_epics()
    api_ingest_epics_issues()
    api_ingest_issues()
    return "done!"
    
@app.route('/api/ingest/epics')
def api_ingest_epics():
    all_epics = epicsModel.fetch_epics()
    epic_issues = all_epics['epic_issues']

    epicsModel.delete_all_epics_for_board()

    for epic_issue in epic_issues:
        epic_issue_number = epic_issue['issue_number']
        epic_issue_details = issuesModel.fetch_issue(epic_issue_number)
        epicsModel.insert_epics(epic_issue_number, epic_issue_details['title'], app.config['REPOS'])

    return "epics ingestion is complete"


@app.route('/api/ingest/epicsIssues')
def api_ingest_epics_issues():
    all_epics = epicsModel.get_epics()
    epicsIssuesModel.delete_all_epics_issues_for_board()
    issuesModel.delete_all_issues_for_board()

    for epic in all_epics["epics"]:
        epic_issues = epicsIssuesModel.fetch_epic_issues(epic["epicId"])
        for issue in epic_issues["issues"]:
            issue_number = issue["issue_number"]
            epicsIssuesModel.insert_epics_issues(epic["epicId"], issue_number, app.config['REPOS'])
            issue_does_not_exists = issuesModel.check_issue_exists(issue_number, app.config['REPOS'])
            if issue_does_not_exists:
                issue_status = issuesModel.fetch_issue_status(issue_number)
                if issue_status is not "epic":
                    issue_details = issuesModel.fetch_issue(issue_number)
                    issuesModel.insert_issues(issue_number, app.config['REPOS'], issue_details['title'], issue_status, issue_details["html_url"])
    return "epics issues ingestion complete"

@app.route('/api/ingest/issues')
def api_ingest_issues():
    # this is to ingest those individual issues and are not part of an epic
    # It can be found in the projectEpicsAndTickets table where type issue
    all_issues = peatm.get_all_issues_from_project(app.config['REPOS'])
    for issue in all_issues:
        issue_number = issue[2]
        issue_status = issuesModel.fetch_issue_status(issue_number)
        if issue_status is not "epic":
            issue_details = issuesModel.fetch_issue(issue_number)
            issuesModel.insert_issues(issue_number, app.config['REPOS'], issue_details['title'], issue_status, issue_details["html_url"])

    return 'ingested issues without Epic individually'
    # VUK010960
    # 07776824548
