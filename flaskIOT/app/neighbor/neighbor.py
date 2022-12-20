from flask import Blueprint

neighbor_blueprint = Blueprint('neighbor', __name__, template_folder='templates')
@neighbor_blueprint.route('/')
def main():
    return '<h1>Neighbor Search</h1>'

    #tra tutti i bidoni che non sono previsti pieno per oggi prendo quello la cui distanza è minore usando API MAPS/HERE