from flask import Blueprint
from flask import request
from app.database.tables import Apartment, Bin, BinRecord
from app.database.__init__ import db
import requests
import numpy as np
import sys
  
neighbor_blueprint = Blueprint('neighbor', __name__, template_folder='templates')
@neighbor_blueprint.route('/')
def main():
    return '<h1>Neighbor Search</h1>'

@neighbor_blueprint.route('/getneighbor', methods=['POST'])  
def getneighbor(): 
    msgJson = request.get_json()
    id_bin = msgJson["id_bin"]
    apartment_ID = Bin.query.filter(Bin.id_bin==id_bin)[0].apartment_ID
    lat_bin= Apartment.query.filter(Apartment.apartment_name==apartment_ID)[0].lat
    long_bin= Apartment.query.filter(Apartment.apartment_name==apartment_ID)[0].lng
    tipologia = Bin.query.filter(Bin.id_bin == id_bin).first().tipologia
    apartments = Apartment.query.all()
    bins = Bin.query.filter(Bin.tipologia==tipologia)
    for bin in bins:
        ultimo_bin_record = BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin).order_by(BinRecord.timestamp.desc()).first()
        if(ultimo_bin_record is None):
            status=None
        else:
            status= ultimo_bin_record.status
        if (status == 1):
            None

    coordinates=[] 
    index=0
    i=0
    for apartment in apartments:
        apartment_coordinate=[]
        if(apartment.lng==long_bin and apartment.lat == lat_bin): 
            index = i
        apartment_coordinate.append(apartment.lng)
        apartment_coordinate.append(apartment.lat)
        coordinates.append(apartment_coordinate)
        i=i+1
    body = {"locations": coordinates}

    headers = {
        'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
        'Content-Type': 'application/json; charset=utf-8'
    }
    call = requests.post('https://ors.gmichele.it/ors/v2/matrix/driving-car', json=body, headers=headers)
    call = call.json()
   
    distances = call["durations"][index]
    minimum= sys.float_info.max
    index_vicino = 0
    for i in range(0, len(distances)):
        if(distances[i]<minimum and distances[i]):
            index_vicino= i
            minimum=distances[i]
    return apartments[index_vicino].street + " " + str(apartments[index_vicino].apartment_street_number)

    
