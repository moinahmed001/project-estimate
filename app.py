from flask import Flask, escape, request, Blueprint, redirect, url_for
from views import views_routes
from ingestApi import ingest_api_routes
import epicsModel, issuesModel, projectEpicsAndTicketsModel as peatm, projectsModel, epicsIssuesModel, ticketsModel, userProjectAccessModel, reportingModel, epicsIssuesRemovedModel, contingencyModel, boardsModel
from flask import jsonify


app = Flask(__name__)
app.register_blueprint(views_routes)
app.register_blueprint(ingest_api_routes)
app.config.from_pyfile('config.cfg')

@app.route('/')
def all_available_urls():
    routes = []
    for route in app.url_map.iter_rules():
        routes.append('{url: %s}' % route)
    return jsonify(routes)



@app.route('/api/post/project', methods=['GET', 'POST'])
def api_post_project():
    response = {}
    response["status"] = "error"
    if request.method == 'POST':
        # validate the form
        if projectsModel.validate_form(request.form):
            # check if the project already exists
            if projectsModel.get_project(request.form)["projects"] == []:

                # check if the board name is valid
                if boardsModel.get_board(request.form["repoId"])["boards"] != []:
                    projectsModel.insert_project(request.form)
                    project_id = projectsModel.get_project(request.form)["projects"][0]["projectId"]
                    url_created = 'views_routes.projectEpicsAndTickets'
                    response["redirectUrl"] = url_for(url_created, project_id=project_id)
                    response["status"] = "success"
                else:
                    response["message"] = "could not find the board "

            else:
                response["message"] = "This project already exists"

        else:
            response["message"] = "failed to validate the form"
            # response["projectData"] = request.form
            response["redirectUrl"] = url_for('views_routes.project')
    else:
        response["message"] = "request was not a POST "
        response["redirectUrl"] = url_for('views_routes.project')

    return jsonify(response)

@app.route('/api/post/projectEpicsAndTickets', methods=['GET', 'POST'])
def api_post_project_epics_and_tickets():
    response = {}
    response["status"] = "error"
    if request.method == 'POST':
        # validate the form
        if peatm.validate_form(request.form):
            # check if the projectEpicsAndTickets already has this epic in the db
            if peatm.get_epic_and_issue(request.form["projectId"], request.form["id"], request.form["type"])["projectEpicsAndTickets"] == []:
                peatm.insert_epic_and_issue(request.form)

                url_created = 'views_routes.projectEpicsAndTickets'
                response["redirectUrl"] = url_for(url_created, project_id=request.form["projectId"])
                response["status"] = "success"
            else:
                response["message"] = "This project epic/issue already exists"
        else:
            response["message"] = "failed to validate the form"
            # response["projectData"] = request.form
            response["redirectUrl"] = url_for('views_routes.project')
    else:
        response["message"] = "request was not a POST "
        response["redirectUrl"] = url_for('views_routes.project')

    return jsonify(response)



@app.route('/api/epics')
def api_epics():
    return jsonify(epicsModel.get_epics())

@app.route('/api/boards')
def api_boards():
    return jsonify(boardsModel.get_boards())

@app.route('/api/issues')
def api_issues():
    return jsonify(issuesModel.get_issues())

@app.route('/api/projectEpicsAndTickets')
def api_project_epics_and_tickets():
    return jsonify(peatm.get_epics_and_issues())

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
def api_epic_issues(board_name, epic_number):
    return epicsIssuesModel.get_epic_issues(board_name, epic_number)

@app.route('/api/epicIssuesFullDetails/<board_name>/<epic_number>')
def api_epic_issues_full_details(board_name, epic_number):
    return epicsIssuesModel.get_epic_issues_full_details(board_name, epic_number)
