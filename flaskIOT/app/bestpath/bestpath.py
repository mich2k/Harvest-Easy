from flask import Blueprint
from app.database.tables import Apartment, Bin, BinRecord
from flask import render_template
import requests
from os import getenv
import datetime
import json
from flask import jsonify
from flasgger import swag_from

OPENROUTESERVICE_KEY = getenv("OPENROUTESERVICE_KEY")
path_blueprint = Blueprint("path", __name__, template_folder="templates")


@path_blueprint.route("/")
def main():
    return "<h1>Best Path</h1>"

# ottenere la matrice delle distanze tra gli appartamenti

@path_blueprint.route("/getdistances")
def getdistances():
    apartments = Apartment.query.all()
    coordinates = []

    for apartment in apartments:
        apartment_coordinate = []
        apartment_coordinate.append(apartment.lng)
        apartment_coordinate.append(apartment.lat)
        coordinates.append(apartment_coordinate)

    body = {"locations": coordinates}

    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Content-Type": "application/json; charset=utf-8",
    }
    
    call = requests.post(
        "https://ors.gmichele.it/ors/v2/matrix/driving-car", json=body, headers=headers
    )
    
    return call.json()


# cammino con solo inizio
@path_blueprint.route("/optimal_route/<float:lat>&<float:lng>")
# @swag_from('/docs/optimal_route.yml')
def optimal_route(lat, lng):
    if (isinstance(lat, float) and isinstance(lng, float)):
        start = [lng, lat]
    else:
        return jsonify({"Errore: latitudine o longitudine scorretti"}), 401

    bins = Bin.query.all()
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
            empty = {}
            empty["apartment_ID"] = bin.apartment_ID
            empty["bin"] = bin.tipologia
            to_empty.append(empty)

    jobs = []
    i = 0
    j = 0
    while i < len(to_empty):
        apartment_ID = to_empty[i]["apartment_ID"]
        apartment = Apartment.query.filter(
            Apartment.apartment_name == apartment_ID).first()
        apartment_coordinate = []
        apartment_coordinate.append(apartment.lng)
        apartment_coordinate.append(apartment.lat)
        job = {"id": j + 1, "location": apartment_coordinate}
        jobs.append(job)
        i = i + 1
        j = j + 1
        if i < len(to_empty):
            while (to_empty[i]["apartment_ID"] == apartment_ID):
                i = i + 1

    body = {
        "jobs": jobs,
        "vehicles": [{
            "id": 1,
            "profile": "driving-car",
            "start": start
        }]
    }
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": OPENROUTESERVICE_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }
    call = requests.post(
        "https://api.openrouteservice.org/optimization", json=body, headers=headers
    )
    call = call.json()
    viewmap(call["routes"][0]["steps"])
    # API json
    best_path = {}
    best_path["duration"] = call["routes"][0]["duration"]
    best_path["steps"] = []

    for i in range(len(call["routes"][0]["steps"])):
        step = {}
        step["arrival"] = call["routes"][0]["steps"][i]["arrival"]
        step["location"] = call["routes"][0]["steps"][i]["location"]
        if (call["routes"][0]["steps"][i]["type"] == "start"):
            step["type"] = "start"
        else:
            step["apartment_ID"] = (
                Apartment.query.filter(
                    Apartment.lat == call["routes"][0]["steps"][i]["location"][1])
                .filter(Apartment.lng == call["routes"][0]["steps"][i]["location"][0])
                .first()
                .apartment_name
            )
            step["bins"] = ""
            for j in range(len(to_empty)):
                if (to_empty[j]["apartment_ID"] == step["apartment_ID"]):
                    step["bins"] += to_empty[j]["bin"] + " "

            step["type"] = "step"

        best_path["steps"].append(step)

    return best_path

# cammino con inizio e fine


@path_blueprint.route("/optimal_route/<float:lat_init>&<float:lng_init>&<float:lat_end>&<float:lng_end>")
def optimal_route2(lat_init, lng_init, lat_end, lng_end):
    if (isinstance(lat_end, float) and isinstance(lng_end, float) and isinstance(lat_init, float) and isinstance(lng_init, float)):
        end = [lng_end, lat_end]
        start = [lng_init, lat_init]
    else:
        return jsonify({"Errore: latitudine e longitudine scorretti"}), 401

    bins = Bin.query.all()
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
            empty = {}
            empty["apartment_ID"] = bin.apartment_ID
            empty["bin"] = bin.tipologia
            to_empty.append(empty)

    jobs = []
    i = 0
    j = 0
    while i < len(to_empty):
        apartment_ID = to_empty[i]["apartment_ID"]
        apartment = Apartment.query.filter(
            Apartment.apartment_name == apartment_ID).first()
        apartment_coordinate = []
        apartment_coordinate.append(apartment.lng)
        apartment_coordinate.append(apartment.lat)
        job = {"id": j + 1, "location": apartment_coordinate}
        jobs.append(job)
        i = i + 1
        j = j + 1
        if i < len(to_empty):
            while (to_empty[i]["apartment_ID"] == apartment_ID):
                i = i + 1

    body = {
        "jobs": jobs,
        "vehicles": [{
            "id": 1,
            "profile": "driving-car",
            "start": start,
            "end": end
        }]
    }
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": OPENROUTESERVICE_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }
    call = requests.post(
        "https://api.openrouteservice.org/optimization", json=body, headers=headers
    )
    call = call.json()
    viewmap(call["routes"][0]["steps"])
    # API json
    best_path = {}
    best_path["duration"] = call["routes"][0]["duration"]
    best_path["steps"] = []

    for i in range(len(call["routes"][0]["steps"])):
        step = {}
        step["arrival"] = call["routes"][0]["steps"][i]["arrival"]
        step["location"] = call["routes"][0]["steps"][i]["location"]
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
            step["bins"] = ""
            for j in range(len(to_empty)):
                if (to_empty[j]["apartment_ID"] == step["apartment_ID"]):
                    step["bins"] += to_empty[j]["bin"] + " "
            step["type"] = "step"

        best_path["steps"].append(step)

    return best_path

# cammino con solo inizio per una certa tipologia di bidoni


@path_blueprint.route("/optimal_route/<float:lat>&<float:lng>&<string:tipologia>")
def optimal_route3(lat, lng, tipologia):
    if (isinstance(lat, float) and isinstance(lng, float)):
        start = [lng, lat]
    else:
        return jsonify({"Errore: latitudine e longitudine scorretti"}), 401

    bins = Bin.query.filter(Bin.tipologia == tipologia)
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
            empty = {}
            empty["apartment_ID"] = bin.apartment_ID
            empty["bin"] = bin.tipologia
            to_empty.append(empty)

    jobs = []
    i = 0
    j = 0
    while i < len(to_empty):
        apartment_ID = to_empty[i]["apartment_ID"]
        apartment = Apartment.query.filter(
            Apartment.apartment_name == apartment_ID).first()
        apartment_coordinate = []
        apartment_coordinate.append(apartment.lng)
        apartment_coordinate.append(apartment.lat)
        job = {"id": j + 1, "location": apartment_coordinate}
        jobs.append(job)
        i = i + 1
        j = j + 1
        if i < len(to_empty):
            while (to_empty[i]["apartment_ID"] == apartment_ID):
                i = i + 1

    body = {
        "jobs": jobs,
        "vehicles": [{
            "id": 1,
            "profile": "driving-car",
            "start": start
        }]
    }
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": OPENROUTESERVICE_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }
    call = requests.post(
        "https://api.openrouteservice.org/optimization", json=body, headers=headers
    )
    call = call.json()
    viewmap(call["routes"][0]["steps"])
    # API json
    best_path = {}
    best_path["duration"] = call["routes"][0]["duration"]
    best_path["tipologia"] = tipologia
    best_path["steps"] = []

    for i in range(len(call["routes"][0]["steps"])):
        step = {}
        step["arrival"] = call["routes"][0]["steps"][i]["arrival"]
        step["location"] = call["routes"][0]["steps"][i]["location"]
        if (call["routes"][0]["steps"][i]["type"] == "start"):
            step["type"] = "start"
        else:
            step["apartment_ID"] = (
                Apartment.query.filter(
                    Apartment.lat == call["routes"][0]["steps"][i]["location"][1])
                .filter(Apartment.lng == call["routes"][0]["steps"][i]["location"][0])
                .first()
                .apartment_name
            )
            step["type"] = "step"

        best_path["steps"].append(step)

    return best_path


# cammino con inizio e fine per una certa tipologia di bidoni
@path_blueprint.route("/optimal_route/<float:lat_init>&<float:lng_init>&<float:lat_end>&<float:lng_end>&<string:tipologia>")
def optimal_route4(lat_init, lng_init, lat_end, lng_end, tipologia):
    if (isinstance(lat_end, float) and isinstance(lng_end, float) and isinstance(lat_init, float) and isinstance(lng_init, float)):
        end = [lng_end, lat_end]
        start = [lng_init, lat_init]
    else:
        jsonify({"Errore: latitudine e longitudine scorretti"}), 401

    bins = Bin.query.filter(Bin.tipologia == tipologia)
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
            empty = {}
            empty["apartment_ID"] = bin.apartment_ID
            empty["bin"] = bin.tipologia
            to_empty.append(empty)

    jobs = []
    i = 0
    j = 0
    while i < len(to_empty):
        apartment_ID = to_empty[i]["apartment_ID"]
        apartment = Apartment.query.filter(
            Apartment.apartment_name == apartment_ID).first()
        apartment_coordinate = []
        apartment_coordinate.append(apartment.lng)
        apartment_coordinate.append(apartment.lat)
        job = {"id": j + 1, "location": apartment_coordinate}
        jobs.append(job)
        i = i + 1
        j = j + 1
        if i < len(to_empty):
            while (to_empty[i]["apartment_ID"] == apartment_ID):
                i = i + 1

    body = {
        "jobs": jobs,
        "vehicles": [{
            "id": 1,
            "profile": "driving-car",
            "start": start,
            "end": end
        }]
    }
    headers = {
        "Accept": "application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8",
        "Authorization": OPENROUTESERVICE_KEY,
        "Content-Type": "application/json; charset=utf-8",
    }
    call = requests.post(
        "https://api.openrouteservice.org/optimization", json=body, headers=headers
    )
    call = call.json()
    viewmap(call["routes"][0]["steps"])
    # API json
    best_path = {}
    best_path["duration"] = call["routes"][0]["duration"]
    best_path["tipologia"] = tipologia
    best_path["steps"] = []

    for i in range(len(call["routes"][0]["steps"])):
        step = {}
        step["arrival"] = call["routes"][0]["steps"][i]["arrival"]
        step["location"] = call["routes"][0]["steps"][i]["location"]
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
            step["type"] = "step"

        best_path["steps"].append(step)

    return best_path

# aggiorno il file path.json con il cammino corrente


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

    with open("./app/bestpath/templates/path.json", "w") as outfile:
        json.dump(viewmap, outfile)

    # return viewmap


@path_blueprint.route("/viewmap")
def getmap():
    return render_template("viewmap.html")
