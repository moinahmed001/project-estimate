from flask import Blueprint, render_template

views_routes = Blueprint('views_routes', __name__)

@views_routes.route('/test')
def test():
    return 'it works!'

@views_routes.route('/test1')
def index():
    return render_template("index.html")
