from flask import Blueprint
import requests
from os import getenv
from app.database.tables import Apartment, BinRecord, Bin
from app.database.__init__ import db
import json
from sqlalchemy.sql.expression import func
import datetime

HERE_API_KEY = getenv('HERE_KEY')

map_blueprint = Blueprint('map', __name__, template_folder='templates')

@map_blueprint.route('/')
def main():
    return '<h1>Map</h1>'

#MAPPA COMPLETA CON TUTTI I BIDONI
@map_blueprint.route('/getmap')
def getpoints(): 
    apartments = Apartment.query.all()
    
    #per ogni bidone nella lista creo un dizionario con le informazioni del bidone da visualizzare sulla mappa
    points=[] #lista di json=punti
    point={}
    for apartment in apartments:
        #prendo i bidoni associati a quell'appartamento 
        bins = Bin.query.filter_by(Bin.apartment_ID == apartment.apartment_ID) 
        for bin in bins: 
            #aggiungo i bidoni dell'appartamento alla mappa come punti
            point['id'] = bin.id_bin
            point['tipologia']=bin.tipologia
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

#MAPPA CON I BIDONI DI UNA CERTA TIPOLOGIA   
@map_blueprint.route('/getmap/<string:tipologia>')
def getpoints(tipologia): 
    apartments = Apartment.query.all()
    
    #per ogni bidone nella lista creo un dizionario con le informazioni del bidone da visualizzare sulla mappa
    points=[] #lista di json=punti
    point={}
    for apartment in apartments:
        #prendo i bidoni associati a quell'appartamento  di quella tipologia
        bins = Bin.query.filter_by(Bin.apartment_ID==apartment.apartment_ID and Bin.tipologia==tipologia) 
        for bin in bins: 
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