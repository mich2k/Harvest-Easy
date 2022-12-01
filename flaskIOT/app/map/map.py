from flask import Blueprint
import requests
from os import getenv
from app.database.database import database_blueprint
import json
import requests

app.register_blueprint(database_blueprint, url_prefix='/database')

HERE_API_KEY = getenv('HERE_KEY')

map_blueprint = Blueprint('map', __name__, template_folder='templates')

@map_blueprint.route('/')
def main():
    return '<h1>Map</h1>'


@map_blueprint.route('/getposition')
def main(): 
    #richiesta A HERE PER OTTENERE LAT E LONG DELL'APPARTAMENTO, per ogni appartamento presente nel database
    HERE_API_URL = f'GET https://geocode.search.hereapi.com/v1/geocode'
    #lista degli appartamenti gestiti dal db
    apartments = Apartment.query.order_by(Apartment.id.desc()).all()
    for apartment in apartments:
        address = apartment.city + apartment.street + apartment.apartment_street_number 
        params = {
            'address': address + 'italia', 
            'apiKey': HERE_API_KEY
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
        #prendo la lista di bidoni associata a quell'appartamento attraverso l'id del bin group
        associated_bingroup = apartment.associated_bingroup
        elencobin = db.session.query(BinRecord).filter_by(associated_bingroup = associated_bingroup)
        
        #per ogni bidone nella lista creo un dizionario con le informazioni del bidone da visualizzare sulla mappa
        points=[]
        point={}

        for i in len(elencobin):
            point['id'] = elencobin[i].id_bin
            point['apartment_name'] = apartment.apartment_name
            point['status'] = elencobin[i].status
            point['address'] = address
            point['riempimento'] = elencobin[i].riempimento
            point['lat'] = lat
            point['lng'] = lng
            #trasformo il dizionario in json
            point = json.dumps(point)
            #aggiungo il json alla lista di punti
            points[i]=point

        viewmap = {
            "updated":"20/11/2022 11:13:06", #mettete ora attuale
            "listaPunti": points
        }
        #DA SALVARE COME FILE JSON PERCHE VIEWMAP LO CARICA PER COSTRUIRE MAPPA
        # Result => Link Rd, Best Nagar, Goregaon West, Mumbai, Maharashtra 400104, India. (lat, lng) = (19.1528967, 72.8371262)