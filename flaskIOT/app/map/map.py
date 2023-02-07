from flask import Blueprint
from app.database.tables import Apartment, Bin, BinRecord
from app.utils.utils import Utils
import json
from flask import render_template
import datetime
from flask import jsonify
from flasgger import swag_from

map_blueprint = Blueprint("map", __name__, template_folder="templates")


def get_points(bin_type = None, sel_city = None, to_be_emptied = False):

    if Bin.query.filter(Bin.tipologia == bin_type).first() == None and bin_type is not None:
        return jsonify({"error": "Tipologia non valida"}), 402

    apartments = Apartment.query.all()
    points = []

    for apartment in apartments:
        bins = Bin.query.filter(Bin.apartment_ID == apartment.apartment_name)        
        
        """if sel_city is not None:
            bins = bins.where(Bin.apartment_ID.in_(Apartment.query.filter(Apartment.city == sel_city)))
            
        elif bin_type is not None:
            bins = bins.where(Bin.tipologia == bin_type)
            
        elif to_be_emptied:
            pass"""
        
        for bin in bins:
            point = {}

            last_bin_record = (
                BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
                .order_by(BinRecord.timestamp.desc())
                .first()
            )

            status = None if last_bin_record is None else last_bin_record.status
            filling = None if last_bin_record is None else last_bin_record.riempimento
            
            
            point["tipologia"] = bin.tipologia
            point["apartment_name"] = apartment.apartment_name
            point["status"] = Utils.getstringstatus(status)
            point["id"] = bin.id_bin
            point["address"] = (
                apartment.street + " " + str(apartment.apartment_street_number) + ", " + apartment.city)
            point["lat"] = apartment.lat
            point["lng"] = apartment.lng
            point["previsione"] = bin.previsione_status
            point["riempimento"] = filling
            
            points.append(point)

    viewmap = {
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "listaPunti": points,
    }

    return jsonify(viewmap)


@map_blueprint.route("/")
def main():
    return "<h1>Map</h1>"


# MAPPA COMPLETA CON TUTTI I BIDONI
@map_blueprint.route("/getmap")
@swag_from('docs/getmap.yml')
def getmap():
    return get_points()


"""@map_blueprint.route("/getmap/<string:type>&<string:city>")
@swag_from('docs/map.yml')
def getmaptipology(type, city):
    return get_points(bin_type=type, sel_city=city)"""

@map_blueprint.route("/viewmap")
def viewmap():
    return render_template("viewmap.html")
