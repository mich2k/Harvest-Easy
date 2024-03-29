from flask import Blueprint
from app.database.tables import Apartment, Bin, BinRecord
import requests
import sys
from flask import jsonify
from flasgger import swag_from
from os import getenv

neighbor_blueprint = Blueprint(
    "neighbor", __name__, template_folder="templates")

OPENROUTESERVICE_KEY = getenv("OPENROUTESERVICE_KEY")


@neighbor_blueprint.route("/")
def main():
    return "<h1>Neighbor Search</h1>"


@neighbor_blueprint.route("/getneighbor/<int:id_bin>", methods=["GET"])
@swag_from('neighbor.yml')
def getneighbor(id_bin):
    """
    questo end point restituisce l'appartamento più vicino con un bidone in stato non pieno
    e non manomesso della stessa tipologia del bidone di input. 
    Ritorna un json con nome dell'appartamento, via, numero, latitudine, longitudine
    """
    if id_bin is None:
        return jsonify({"error": "Id_bin not correct"}), 401

    bin = Bin.query.filter(Bin.id_bin == id_bin).first()

    if bin == None:
        return jsonify({"error": "Bin doesn't exist"}), 402

    # dati del bidone pieno
    apartment_ID = Bin.query.filter(Bin.id_bin == id_bin)[0].apartment_ID
    lat_bin = Apartment.query.filter(
        Apartment.apartment_name == apartment_ID)[0].lat
    long_bin = Apartment.query.filter(
        Apartment.apartment_name == apartment_ID)[0].lng
    tipologia = Bin.query.filter(Bin.id_bin == id_bin).first().tipologia

    apartments = Apartment.query.all()
    # bidoni di quella tipologia
    bins = Bin.query.filter(Bin.tipologia == tipologia)

    apartments_ID = []  # nomi appartamenti con bidoni di quella tipologia non pieni
    # aggiungo l'appartamento del bidone pieno
    apartments_ID.append(apartment_ID)
    for bin in bins:
        ultimo_bin_record = (
            BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
            .order_by(BinRecord.timestamp.desc())
            .first()
        )

        status = None if ultimo_bin_record is None else ultimo_bin_record.status

        if status == 1:
            apartments_ID.append(bin.apartment_ID)

    coordinates = (
        []
    )  # coordinate degli appartamenti con bidoni non pieni della stessa tipologia da cui calcolare la distanza, compreso quello di origine

    index = 0  # indice del mio appartamento nella lista

    for i in range(len(apartments)):
        apartment_coordinate = []
        if apartments[i].apartment_name in apartments_ID:
            if apartments[i].lng == long_bin and apartments[i].lat == lat_bin:
                index = i

            apartment_coordinate.append(apartments[i].lng)
            apartment_coordinate.append(apartments[i].lat)
            coordinates.append(apartment_coordinate)

    if (len(coordinates) < 2):
        return 'Nessun vicino disponibile'

    body = {"locations": coordinates}

    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": OPENROUTESERVICE_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }

    call = requests.post(
        'https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers).json()
    # https://ors.gmichele.it/ors/v2/matrix/driving-car

    if 'error' in call:
        return 'error: ' + str(call)

    distances = call["durations"][index]

    # calcolo del vicino
    minimum = sys.float_info.max
    index_vicino = 0
    for i in range(len(distances)):
        if distances[i] < minimum and distances[i]:
            index_vicino = i
            minimum = distances[i]

    apartment_name = (
        Apartment.query.filter(Apartment.lat == coordinates[index_vicino][1])
        .filter(Apartment.lng == coordinates[index_vicino][0])
        .first()
        .apartment_name
    )

    vicino = Apartment.query.filter(
        Apartment.apartment_name == apartment_name).first()

    return jsonify({"street": vicino.street,  "number": vicino.apartment_street_number, "apartment_name": vicino.apartment_name,
                    "lat": vicino.lat, "lng": vicino.lng}), 200
