from flask import Blueprint
from app.database.tables import Apartment, Bin, BinRecord
from app.utils.utils import Utils
from flask import render_template
import datetime
from flask import jsonify
from flasgger import swag_from

map_blueprint = Blueprint(
    "map", __name__, template_folder="templates", static_folder='static')

utility = Utils()

def get_points(bin_type=None, sel_city=None, to_be_emptied=False):

    if Bin.query.filter(Bin.tipologia == bin_type).first() == None and bin_type is not None:
        return jsonify({"error": "Tipologia non valida"}, 402)

    apartments = Apartment.query.all(
    ) if sel_city is None else Apartment.query.filter(Apartment.city == sel_city).all()
    points = []

    for apartment in apartments:
        bins = Bin.query.filter(Bin.apartment_ID == apartment.apartment_name).all()

        if bin_type is not None:
            bins = bins.filter(Bin.tipologia == bin_type)

        for bin in bins:
            point = {}

            last_bin_record = BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin).order_by(
                BinRecord.timestamp.desc()).first()

            if to_be_emptied and (utility.calcolastatus(bin.id_bin, last_bin_record.riempimento) == 1 or utility.calcolastatus(bin.id_bin, last_bin_record.riempimento) == 3):
                continue

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
            point["previsione"] = bin.previsione_status if bin.previsione_status != "" else "Not avaible yet"
            point["riempimento"] = filling

            points.append(point)

    viewmap = {
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "listaPunti": points,
    }
    print(viewmap)
    return jsonify(viewmap)


@map_blueprint.route("/")
def main():
    return "<h1>Map</h1>"


# MAPPA COMPLETA CON TUTTI I BIDONI
@map_blueprint.route("/getmap")
@swag_from('docs/getmap.yml')
def get_map():
    return get_points()

# Mappa di tutti i bidoni di una città


@map_blueprint.route("/getmap/<string:city>")
def getmapfromcity(city):
    return get_points(sel_city=city)

# Mappa di tutti i bidoni di un certo tipo di una città


@map_blueprint.route("/getmap/<string:type>&<string:city>")
@swag_from('docs/map.yml')
def get_filteredmap(type, city):
    return get_points(bin_type=type, sel_city=city)

# Servizi per lo svuotamento dei bidoni pieni, stessi filtri di prima ma verranno considerati solo i bidoni pieni


@map_blueprint.route("/getservicemap")
def get_servicemap():
    return get_points(to_be_emptied=True)


@map_blueprint.route("/getservicemap/<string:type>&<string:city>")
def get_servicefilteredmap(type, city):
    return get_points(bin_type=type, sel_city=city, to_be_emptied=True)

# Mappa completa per Utenti


@map_blueprint.route("/viewmap")
def viewmap():
    return render_template("viewmap.html", path='getmap')

# Mappa per HERA che filtra in base alla città


@map_blueprint.route("/viewmapservice")
def viewmapservice():
    return render_template("viewmap.html", path='getservicemap')
