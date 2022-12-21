from flask import Blueprint
from flask import Flask
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from app.database.tables import Apartment, Bin
from os import getenv
from flask import render_template

# you can set key as config
GOOGLEMAPS_KEY = getenv('GOOGLEMAPS_KEY')

path_blueprint = Blueprint('path', __name__, template_folder='templates')
@path_blueprint.route('/')
def main():
    return '<h1>Best Path</h1>'

@path_blueprint.route('/map')
def mapview():
    # creating a map in the view
    apartments = Apartment.query.all()
    point={}
    points=[]
    for apartment in apartments:
        #prendo i bidoni associati a quell'appartamento 
        bins = Bin.query.filter_by(Bin.apartment_ID == apartment.apartment_ID) 
        for bin in bins: 
            #aggiungo i bidoni dell'appartamento alla mappa come punti
            point['lat'] = apartment.lat
            point['lng'] = apartment.lng
            point['label'] = bin.tipologia
            points.append(point)

    map = Map(
        identifier="sndmap",
        lat=44.645957,
        lng=10.925629,
        markers=points #markers: a list of dicts containing lat, lng, icon, label.
        #markers=[(point['lat'], point['lat']) for point in points]
    )
    return render_template('map.html', map=map)
