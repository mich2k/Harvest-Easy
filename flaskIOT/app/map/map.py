from flask import Blueprint
from app.database.tables import Apartment, Bin, BinRecord
from app.utils.utils import Utils
from flask import render_template
import datetime
from os import getenv
from flask import jsonify
from flasgger import swag_from

map_blueprint = Blueprint(
    "map", __name__, template_folder="templates", static_folder='static')

utility = Utils()
URL = getenv('URL_map')


@map_blueprint.route("/getmap")
@map_blueprint.route("/getmap/<string:sel_city>")
@map_blueprint.route("/getmap/<string:bin_type>&<string:sel_city>")
def get_points(bin_type=None, sel_city=None, to_be_emptied=False):

    if Bin.query.filter(Bin.tipologia == bin_type).first() == None and bin_type is not None:
        return jsonify({"error": "Tipologia non valida"}), 401

    if sel_city is not None:
        if Apartment.query.filter(Apartment.city == sel_city).all() is None:
            return jsonify({"error": "Città non valida"}), 402

    apartments = Apartment.query.all(
    ) if sel_city is None else Apartment.query.filter(Apartment.city == sel_city).all()
    points = []

    for apartment in apartments:
        bins = Bin.query.filter(
            Bin.apartment_ID == apartment.apartment_name).all()

        if bin_type is not None:
            bins = Bin.query.filter(
                Bin.apartment_ID == apartment.apartment_name).filter(Bin.tipologia == bin_type).all()

        for bin in bins:
            point = {}

            last_bin_record = BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin).order_by(
                BinRecord.timestamp.desc()).first()

            status = None if last_bin_record is None else last_bin_record.status

            if to_be_emptied and (status == 1 or status == 3):
                continue

            filling = 'Empty' if last_bin_record is None else last_bin_record.riempimento

            point["tipologia"] = bin.tipologia
            point["apartment_name"] = apartment.apartment_name
            point["status"] = Utils.getstringstatus(status)
            point["id"] = bin.id_bin
            point["address"] = (
                apartment.street + " " + str(apartment.apartment_street_number) + ", " + apartment.city)
            point["lat"] = apartment.lat
            point["lng"] = apartment.lng
            point["previsione"] = bin.previsione_status if bin.previsione_status != "" else "Not avaible yet"
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
@swag_from('docs/getmap.yml')
def get_map():
    return get_points()

# Mappa di tutti i bidoni di una città


@swag_from('docs/getmap2.yml')
def getmapfromcity(city):
    return get_points(sel_city=city)

# Mappa di tutti i bidoni di un certo tipo di una città


@swag_from('docs/getmap3.yml')
def get_filteredmap(type, city):
    return get_points(bin_type=type, sel_city=city)

# Servizi per lo svuotamento dei bidoni pieni, stessi filtri di prima ma verranno considerati solo i bidoni pieni


@map_blueprint.route("/getservicemap")
@swag_from('docs/getservicemap.yml')
def get_servicemap():
    return get_points(to_be_emptied=True)


@map_blueprint.route("/getservicemap/<string:type>&<string:city>")
@swag_from('docs/getservicemap2.yml')
# @swag_from('docs/getservicemap2.yml')
def get_servicefilteredmap(type, city):
    return get_points(bin_type=type, sel_city=city, to_be_emptied=True)


# Mappa per Utenti


@map_blueprint.route("/viewmap")
def viewmap():
    return render_template("viewmap.html", path='getmap')


@map_blueprint.route("/viewmap/<string:city>")
def viewmap2(city):
    return render_template("viewmap.html", path=URL + city)


@map_blueprint.route("/viewmap/<string:type>&<string:city>")
def viewmap3(type, city):
    return render_template("viewmap.html", path=URL + type + '%26' + city)

# Mappa per HERA che filtra in base alla città


@map_blueprint.route("/viewmapservice")
def viewmapservice():
    return render_template("viewmap.html", path='getservicemap')


@map_blueprint.route("/viewmapservice/<string:type>&<string:city>")
def viewmapservice2(type, city):
    return render_template("viewmap.html", path='getservicemap/' + type + '&' + city)
