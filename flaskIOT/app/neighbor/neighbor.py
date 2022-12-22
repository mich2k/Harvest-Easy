from flask import Blueprint

neighbor_blueprint = Blueprint('neighbor', __name__, template_folder='templates')
@neighbor_blueprint.route('/')
def main():
    return '<h1>Neighbor Search</h1>'

