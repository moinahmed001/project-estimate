from flask import Blueprint

views_routes = Blueprint('views_routes', __name__)

@views_routes.route('/test')
def test():
    return 'it works!'
