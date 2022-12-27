from flask import Blueprint
from os import getenv
from app.database.tables import Apartment, Bin, BinRecord
from app.database.__init__ import db
import json
from sqlalchemy.sql.expression import func
import datetime
from flask import jsonify

HERE_API_KEY = getenv('HERE_KEY')

map_blueprint = Blueprint('map', __name__, template_folder='templates')

@map_blueprint.route('/')
def main():
    return '<h1>Map</h1>'

#MAPPA COMPLETA CON TUTTI I BIDONI
@map_blueprint.route('/getmap')
#@map_blueprint.route('/getmap/<string:tipologia>')
def getmap(): 
    apartments = Apartment.query.all()
    #if (tipologia == None):
        
     #   pass

    points=[] #lista di json=punti
    for apartment in apartments:
        bins = Bin.query.filter(Bin.apartment_ID == apartment.apartment_name) 
        for bin in bins:
            point={} 
            #ultimo_bin_record=(BinRecord.query.filter(BinRecord.id_bin==bin.id_bin).order_by(BinRecord.timestamp.desc()))[0]
            status=1 #ultimo_bin_record.status
        
            point['tipologia']= bin.tipologia
            point['apartment_name'] = apartment.apartment_name
            point['status'] = status
            point['id'] = bin.id_bin
            point['address'] = apartment.street + " " + str(apartment.apartment_street_number) + ", " + apartment.city
            point['lat'] = apartment.lat
            point['lng'] = apartment.lng
            point['previsione'] = bin.previsione_status
            points.append(point)
    
    viewmap = {
        "updated": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
        "listaPunti": points
    }

    with open('points.json', 'w') as outfile:
        json.dump(viewmap, outfile)

    return viewmap

@map_blueprint.route('/getmap/<string:tipologia>')
#MAPPA CON I BIDONI DI UNA CERTA TIPOLOGIA   
def getmaptipology(tipologia): 
    apartments = Apartment.query.all()
    
    #per ogni bidone nella lista creo un dizionario con le informazioni del bidone da visualizzare sulla mappa
    points=[] #lista di json=punti
    point={}
    for apartment in apartments:
        #prendo i bidoni associati a quell'appartamento  di quella tipologia
        bins = Bin.query.filter_by(Bin.apartment_ID==apartment.apartment_name, Bin.tipologia==tipologia)
        for bin in bins: 
            ultimo_bin_record=(BinRecord.query.filter(BinRecord.id_bin==bin.id_bin).order_by(BinRecord.timestamp.desc))[0]
            status=ultimo_bin_record.status
            #aggiungo i bidoni dell'appartamento alla mappa come punti
            point['id'] = bin.id_bin
            point['apartment_name'] = apartment.apartment_name
            point['status'] = bin.status
            point['address'] = apartment.city + apartment.street + apartment.apartment_street_number 
            point['lat'] = apartment.lat
            point['lng'] = apartment.lng
            point['previsione'] = bin.previsione_status
            
            #trasformo il dizionario in json
            point = json.dumps(point)
            #aggiungo il json alla lista di punti
            points.append(point)

    viewmap = {
        "updated":datetime.datetime.now, 
        "listaPunti": points
    }

    return viewmap
