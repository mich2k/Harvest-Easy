from flask import Blueprint

geofirstrecord_blueprint = Blueprint('geofirstrecord', __name__, template_folder='templates')

@geofirstrecord_blueprint.route('/')
def main():
    return '<h1>GeoFirstRecord</h1>'