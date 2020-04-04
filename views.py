from flask import Blueprint, render_template

views_routes = Blueprint('views_routes', __name__)

@views_routes.route('/test')
def test():
    return 'it works!'

@views_routes.route('/project')
def project():
    # check if session has error and then display it with the form data
    return render_template("project.html")
