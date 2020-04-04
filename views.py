from flask import Blueprint, render_template
import projectsModel, epicsModel, boardsModel

views_routes = Blueprint('views_routes', __name__)

@views_routes.route('/project')
def project():
    boards = None
    if boardsModel.get_boards()["boards"] != []:
        boards = boardsModel.get_boards()["boards"]
    print(boards)
    # check if session has error and then display it with the form data
    return render_template("project.html", boards=boards)

@views_routes.route('/projectEpicsAndTickets/<int:project_id>')
def projectEpicsAndTickets(project_id):
    project = None
    epics = None
    if projectsModel.get_project_with_id(project_id)["projects"] != []:
        project = projectsModel.get_project_with_id(project_id)["projects"][0]
    if epicsModel.get_epics()["epics"] != []:
        epics = epicsModel.get_epics()["epics"]
    print(project)
    return render_template("projectEpicsAndTickets.html", project=project, epics=epics)
