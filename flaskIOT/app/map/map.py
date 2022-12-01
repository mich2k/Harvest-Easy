from flask import Blueprint
import requests
from os import getenv
from app.database.__init__ import database_blueprint
import json


HERE_API_KEY = getenv('HERE_KEY')
map_blueprint = Blueprint('map', __name__, template_folder='templates')

@map_blueprint.route('/')
def main():
    return '<h1>Map</h1>'


# Simplest way to get the lat, long of any address.

# Using Python requests and the Google Maps Geocoding API.

@map_blueprint.route('/getposition')
def main(): 
    #GET A HERE PER OTTENERE LAT E LONG DELL'APPARTAMENTO
    HERE_API_URL = f'GET https://geocode.search.hereapi.com/v1/geocode'

    apartment = Apartment.query.order_by(Apartment.id.desc()).all()
    #da verificare [0]
    address = apartment[0].city + apartment[0].street + apartment[0].apartment_street_number 

    apartmentname = apartment[0].apartment_name

    params = {
        'address': address + 'italia',
        'apiKey': 'HERE_API_KEY'
    }
    
    # Do the request and get the response data
    req = requests.get(HERE_API_URL, params=params)
    res = req.json()

    # Use the first result
    result = res['object'][0]

    lat = result['items'][0]['position']['lat']
    lng = result['items'][0]['position']['lng']

    print(lat)
    print(lng)

    #VIEW MAP CON BIDONI
    elencobin = BinRecord.query.order_by(Apartment.id.desc()).all()
    points=[]
    
    point={}
    for i in len(elencobin):
        point['id'] = elencobin[i].id_bin
        point['apartment_name'] = apartmentname
        point['status'] = elencobin[i].status
        point['address'] = address
        point['riempimento'] = elencobin[i].riempimento
        point['lat'] = lat
        point['lng'] = lng
        point = json.dumps(point)
        points[i]=point

    viewmap{
        "updated":"20/11/2022 11:13:06", #mettete ora attuale
        "listaPunti": points
    }
    #DA SALVARE COME FILE JSON PERCHE VIEWMAP LO CARICA PER COSTRUIRE MAPPA
    # Result => Link Rd, Best Nagar, Goregaon West, Mumbai, Maharashtra 400104, India. (lat, lng) = (19.1528967, 72.8371262)