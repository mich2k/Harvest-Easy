from flask import Blueprint
from app.database.tables import Apartment, Bin, BinRecord
from app.utils.utils import Utils
import json
from flask import render_template
import datetime
from flask import jsonify
from flasgger import swag_from

map_blueprint = Blueprint("map", __name__, template_folder="templates")


@map_blueprint.route("/")
def main():
    return "<h1>Map</h1>"



# MAPPA COMPLETA CON TUTTI I BIDONI
@map_blueprint.route("/getmap")
@swag_from('docs/getmap.yml')
def getmap():
    apartments = Apartment.query.all()
    points = []
    for apartment in apartments:
        bins = Bin.query.filter(Bin.apartment_ID == apartment.apartment_name)
        for bin in bins:
            point = {}
            ultimo_bin_record = (
                BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
                .order_by(BinRecord.timestamp.desc())
                .first()
            )
            if ultimo_bin_record is None:
                status = None
                riempimento = None
            else:
                status = ultimo_bin_record.status
                riempimento = ultimo_bin_record.riempimento
                status = Utils.getstringstatus(status)
            point["tipologia"] = bin.tipologia
            point["apartment_name"] = apartment.apartment_name
            point["status"] = status
            point["id"] = bin.id_bin
            point["address"] = (
                apartment.street
                + " "
                + str(apartment.apartment_street_number)
                + ", "
                + apartment.city
            )
            point["lat"] = apartment.lat
            point["lng"] = apartment.lng
            point["previsione"] = bin.previsione_status
            point["riempimento"] = riempimento
            points.append(point)

    viewmap = {
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "listaPunti": points,
    }

    with open("./app/map/templates/points.json", "w") as outfile:
        json.dump(viewmap, outfile)

    return viewmap


@map_blueprint.route("/getmap/<string:tipologia>")
@swag_from('docs/map.yml')
def getmaptipology(tipologia):
    if tipologia is None:
        return jsonify({"error": "Tipologia errata"}), 401
    
    if Bin.query.filter(Bin.tipologia == tipologia).first() == None:
        return jsonify({"error": "Tipologia non valida"}), 402

    apartments = Apartment.query.all()
    points = []
    for apartment in apartments:
        bins = Bin.query.filter(Bin.apartment_ID == apartment.apartment_name).filter(
            Bin.tipologia == tipologia
        )
        for bin in bins:
            point = {}
            ultimo_bin_record = (
                BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
                .order_by(BinRecord.timestamp.desc())
                .first()
            )
            if ultimo_bin_record is None:
                status = None
                riempimento = None
            else:
                status = ultimo_bin_record.status
                riempimento = ultimo_bin_record.riempimento
                status = Utils.getstringstatus(status)
            point["apartment_name"] = apartment.apartment_name
            point["status"] = status
            point["id"] = bin.id_bin
            point["address"] = (
                apartment.street
                + " "
                + str(apartment.apartment_street_number)
                + ", "
                + apartment.city
            )
            point["lat"] = apartment.lat
            point["lng"] = apartment.lng
            point["previsione"] = bin.previsione_status
            point["riempimento"] = riempimento
            points.append(point)

    viewmap = {
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "listaPunti": points,
    }

    with open("./app/map/templates/points.json", "w") as outfile:
        json.dump(viewmap, outfile)

    return viewmap

@map_blueprint.route("/viewmap")
def viewmap():
    return render_template("viewmap.html")