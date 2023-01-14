from flask import Blueprint
from app.database.tables import Apartment, Bin
from flask import render_template
import requests
from os import getenv

OPENROUTESERVICE_KEY = getenv('OPENROUTESERVICE_KEY')
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


   
@path_blueprint.route('/optimal_route/<float:lat>&<float:lng>')  
def optimal_route(lat, lng): 
    apartments = Apartment.query.all() 
    jobs=[]
    for i in range (len(apartments)):
        apartment_coordinate=[]
        apartment_coordinate.append(apartments[i].lng)
        apartment_coordinate.append(apartments[i].lat)
        job={"id":i+1,"location":apartment_coordinate}
        jobs.append(job)
    
    body = {"jobs": jobs,
        "vehicles": {"id":1,"profile":"driving-car","start":[lng, lat],"end":[lng, lat]}}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Authorization': OPENROUTESERVICE_KEY,
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://api.openrouteservice.org/optimization', json=body, headers=headers)
    return call.json()
