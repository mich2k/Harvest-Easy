from flask import Blueprint
from app.database.tables import Apartment, Bin, BinRecord
from flask import render_template
import requests
from os import getenv
import datetime
from flask import jsonify
from flasgger import swag_from

OPENROUTESERVICE_KEY = getenv("OPENROUTESERVICE_KEY")
path_blueprint = Blueprint("path", __name__, template_folder="templates")

@path_blueprint.route("/")
def main():
    return "<h1>Best Path</h1>"

# ottenere la matrice delle distanze tra gli appartamenti
# Perchè la usiamo?


@path_blueprint.route("/getdistances")
def getdistances():

    apartments = Apartment.query.all()
    coordinates = []

    for apartment in apartments:
        coordinates.append([apartment.lng, apartment.lat])

    body = {"locations": coordinates}

    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
    }

    call = requests.post(
        "https://ors.gmichele.it/ors/v2/matrix/driving-car", json=body, headers=headers
    )

    return call.json()


@path_blueprint.route("/optimal_route/<float:lat>&<float:lng>")
@path_blueprint.route("/optimal_route/<float:lat>&<float:lng>&<string:type>")
@path_blueprint.route("/optimal_route/<float:lat>&<float:lng>&<float:lat_stop>&<float:lng_stop>")
@path_blueprint.route("/optimal_route/<float:lat>&<float:lng>&<float:lat_stop>&<float:lng_stop>&<string:type>")
# @swag_from('/docs/optimal_route.yml')
def optimal_route(lat, lng, lat_stop=None, lng_stop=None, type=None):

    if (isinstance(lat, float) and isinstance(lng, float)):
        start = [lng, lat]
        end = []

        if lat_stop is not None and lng_stop is not None:

            if isinstance(lat_stop, float) and isinstance(lng_stop, float):
                end.append(lng_stop, lat_stop)

    else:
        # Ritornare response
        return jsonify({"Errore: latitudine o longitudine scorretti"}), 401

    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": OPENROUTESERVICE_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }

    bins = Bin.query.all() if type is None else Bin.query.filter(Bin.tipologia == type)
    to_empty = []  # appartamenti con i relativi bidoni pieni

    for bin in bins:

        ultimo_bin_record = (
            BinRecord.query.filter(BinRecord.associated_bin == bin.id_bin)
            .order_by(BinRecord.timestamp.desc())
            .first()
        )

        if ultimo_bin_record is None:
            status = None

        else:
            status = ultimo_bin_record.status

        if status == 2:
            to_empty.append(
                {"apartment_ID": bin.apartment_ID, "bin": bin.tipologia})

    jobs = []
    id_count = 0

    for i in range(len(to_empty) - 1):

        apartment_ID = to_empty[i]["apartment_ID"]

        apartment = Apartment.query.filter(
            Apartment.apartment_name == apartment_ID).first()

        id_count += 1

        jobs.append({"id": id_count, "location": [
                    apartment.lng, apartment.lat]})

        if to_empty[i + 1]["apartment_ID"] == apartment_ID:
            continue

    body = {
        "jobs": jobs,
        "vehicles": [{
            "id": 1,
            "profile": "driving-car",
            "start": start
        }]
    }
        
    # da testare
    if end:
        body["vehicles"][0]['end'] = end

    call = requests.post(
        "https://api.openrouteservice.org/optimization", json=body, headers=headers).json()
    
    if 'error' in call:
        return 'Error: ' + str(call) 

    
    print(viewmap(call["routes"][0]["steps"]))

    # API json
    best_path = {}
    best_path["duration"] = call["routes"][0]["duration"]
    best_path["steps"] = []

    if type is not None:
        best_path["tipologia"] = type

    for i in range(len(call["routes"][0]["steps"])):

        step = {'arrival': call["routes"][0]["steps"][i]["arrival"],
                'location': call["routes"][0]["steps"][i]["location"]}

        if (call["routes"][0]["steps"][i]["type"] == "start" or call["routes"][0]["steps"][i]["type"] == "end"):
            step["type"] = call["routes"][0]["steps"][i]["type"]

        else:

            step["apartment_ID"] = (
                Apartment.query.filter(
                    Apartment.lat == call["routes"][0]["steps"][i]["location"][1])
                .filter(Apartment.lng == call["routes"][0]["steps"][i]["location"][0])
                .first()
                .apartment_name
            )

            if type is None:

                step["bins"] = ""

                for j in range(len(to_empty)):

                    if (to_empty[j]["apartment_ID"] == step["apartment_ID"]):
                        step["bins"] += to_empty[j]["bin"] + " "

            step["type"] = "step"

        best_path["steps"].append(step)

    return jsonify(best_path)


# Perchè la usiamo?
def viewmap(steps):
    points = []

    for i in range(len(steps)):
        point = {}

        point["id"] = i

        if (steps[i]["type"] == "start" or steps[i]["type"] == "end"):
            point["type"] = steps[i]["type"]
        else:
            point["type"] = "step"

        point["duration"] = steps[i]["duration"]
        point["lat"] = steps[i]["location"][1]
        point["lng"] = steps[i]["location"][0]

        points.append(point)

    viewmap = {
        "updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "listaPunti": points,
    }
    
    # Aggiornare la lista di punti che la mappa stamperà
    
    

# Cosa chiama?


@path_blueprint.route("/viewmap")
def getmap():
    return render_template("viewmap.html", path='/optimal_route')
