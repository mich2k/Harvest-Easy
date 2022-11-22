from flask import Blueprint

map_blueprint = Blueprint('map', __name__, template_folder='templates')
@map_blueprint.route('/')
def main():
    return '<h1>Map</h1>'