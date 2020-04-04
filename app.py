from flask import Flask, escape, request, Blueprint
from views import views_routes
from ingestApi import ingest_api_routes
import epicsModel, issuesModel, projectEpicsAndTicketsModel as peatm, projectsModel, epicsIssuesModel, ticketsModel, userProjectAccessModel, reportingModel, epicsIssuesRemovedModel, contingencyModel
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(views_routes)
app.register_blueprint(ingest_api_routes)
app.config.from_pyfile('config.cfg')

@app.route('/')
def hello():
    routes = []
    print(app.url_map)
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

@app.route('/api/userProjectAccess')
def api_user_project_access():
    return jsonify(userProjectAccessModel.get_user_project_access())

@app.route('/api/reporting')
def api_reporting():
    return jsonify(reportingModel.get_reporting())

@app.route('/api/contingency')
def api_contingency():
    return jsonify(contingencyModel.get_contingency())

@app.route('/api/epicsIssuesRemoved')
def api_epics_issues_removed():
    return jsonify(epicsIssuesRemovedModel.get_epics_issues_removed())

@app.route('/api/issue/<board_name>/<issue_number>')
def api_issue(board_name, issue_number):
    return issuesModel.get_issue(board_name, issue_number)

@app.route('/api/epicsIssues/<board_name>/<epic_number>')
def api_epicsIssues(board_name, epic_number):
    return epicsIssuesModel.get_epic_issues(board_name, epic_number)
