from flask import Blueprint

path_blueprint = Blueprint('path', __name__, template_folder='templates')
@path_blueprint.route('/')
def main():
    return '<h1>Best Path</h1>'