from flask import Blueprint
from os import getenv
from app.database.tables import Apartment, Bin, BinRecord
from app.database.__init__ import db
import json
import datetime
from flask import jsonify
import requests
from os import getenv
import googlemaps

GOOGLEMAPS_API_KEY = getenv('GOOGLEMAPS_API_KEY')
  
neighbor_blueprint = Blueprint('neighbor', __name__, template_folder='templates')
@neighbor_blueprint.route('/')
def main():
    return '<h1>Neighbor Search</h1>'

@neighbor_blueprint.route('/getneighbor/<int:id_bin>')
def getneighbor(id_bin):
    apartment_name=Bin.query.filter(Bin.id_bin==id_bin).first().apartment_ID
    apartment = Apartment.query.filter(Apartment.apartment_name==apartment_name).first()
    address = apartment.street + " " + str(apartment.apartment_street_number) + ", " + apartment.city
    
    origin=[]
    origin.append(address)
    desinations=[]
    apartments = Apartment.query.all()
    for apartment in apartments:
        address = apartment.street + " " + str(apartment.apartment_street_number) + ", " + apartment.city
        desinations.append(address) 
    
    url ='https://maps.googleapis.com/maps/api/distancematrix/json?'
    req = requests.get(url + 'origins = ' + origin +
                   '&destinations = ' + desinations +
                   '&key = ' + GOOGLEMAPS_API_KEY)
    result = req.json()
    return result
    


