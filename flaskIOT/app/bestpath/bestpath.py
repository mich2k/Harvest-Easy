from flask import Blueprint
from flask import Flask
from app.database.tables import Apartment, Bin
from os import getenv
from flask import render_template
import requests

# you can set key as config
#OPENROUTESERVICE_KEY = getenv('OPENROUTESERVICE_KEY')

path_blueprint = Blueprint('path', __name__, template_folder='templates')
@path_blueprint.route('/')
def main():
    return '<h1>Best Path</h1>'


@path_blueprint.route('/getdistances')  
def getdistances(): 
    apartments = Apartment.query.all()
    coordinates=[] 
    
    for apartment in apartments:
        apartment_coordinate=[]
        apartment_coordinate.append(apartment.lng)
        apartment_coordinate.append(apartment.lat)
        coordinates.append(apartment_coordinate)

    body = {"locations": coordinates}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://ors.gmichele.it/ors/v2/matrix/driving-car', json=body, headers=headers)
    return call.json()