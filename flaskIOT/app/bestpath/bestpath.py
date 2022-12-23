from flask import Blueprint
from flask import Flask
from app.database.tables import Apartment, Bin
from os import getenv
from flask import render_template

# you can set key as config
GOOGLEMAPS_KEY = getenv('GOOGLEMAPS_KEY')

path_blueprint = Blueprint('path', __name__, template_folder='templates')
@path_blueprint.route('/')
def main():
    return '<h1>Best Path</h1>'
