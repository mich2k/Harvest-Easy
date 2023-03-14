from datetime import datetime
from flask import Response
from sqlalchemy import update
from os import getenv
from app.database.tables import Apartment, Bin, BinRecord
from ..database.database import db
from ..trap.trap import *
import random
import json
import requests


class Utils:

    HERE_API_KEY = getenv("HERE_KEY")
    WEATHER_KEY = getenv("WEATHER_KEY")
    WEATHERE_API_URL = f"https://api.openweathermap.org/data/2.5/weather"
    dd_umido = {"medie": 5, "alte": 3, "altissime": 2}
    soglie = {
        "plastica": 0.9,
        "carta": 0.9,
        "vetro": 0.8,
        "umido": 0.7,
    }  # soglie fisse

    def __init__(self):
        # self.key = getenv['POST_SECRET_KEY']
        self.key = "maybesupersecretkey"

    def calcolastatus(self, id_bin: int, riempimento: float, roll=0, pitch=90, co2=1000, prophet=False):
        """ 
        Legenda status:
            1: integro e non-pieno, 
            2: integro e pieno, 
            3: manomesso e non-pieno, 
            4: manomesso e pieno
        """

        # soglia dinamica per l'organico in base alla temperatura

        limite_co2 = 2000  # 2000ppm

        # Seleziono il bidone passato
        current_bin = BinRecord.query.filter(
            BinRecord.associated_bin == id_bin)

        # Estraggo lo status corrente o, se non presente, lo imposto di default ad 1 (suppongo un bidone nuovo: integro e vuoto)
        current_status = (
            BinRecord.query.filter(BinRecord.associated_bin == id_bin)
            .order_by(BinRecord.timestamp.desc())
            .first()
        ).status if current_bin.count() else 1

        type = Bin.query.filter(Bin.id_bin == id_bin).first().tipologia

        apartment_ID = (Bin.query.filter(
            Bin.id_bin == id_bin)).first().apartment_ID

        if type == "umido":
            # Mesi caldi
            current_threashold = self.get_organic_threashold(apartment_ID, id_bin) if datetime.now(
            ).month >= 4 and datetime.now().month <= 10 else self.soglie["umido"]

        elif type == "plastica":
            current_threashold = self.soglie["plastica"]

        elif type == "carta":
            current_threashold = self.soglie["carta"]

        elif type == "vetro":
            current_threashold = self.soglie["vetro"]

        if current_status == 1:
            if float(riempimento) >= current_threashold and riempimento is not None:
                if not prophet:
                    report(id_bin, db, apartment_ID, riempimento)
                current_status = 2

            if (abs(roll) >= 30 or (abs(pitch - 90) >= 30)) and roll is not None and pitch is not None:
                if not prophet:
                    report(id_bin, db, apartment_ID, 90)
                current_status = 3

            if co2 >= limite_co2 and co2 is not None:
                if not prophet:
                    report(id_bin, db, apartment_ID, co2)
                current_status = 3

            return current_status

        if current_status == 2:

            if float(riempimento) < current_threashold and riempimento is not None:
                current_status = 1
                db.session.query(Bin).filter(Bin.id_bin == id_bin).update(
                    {"ultimo_svuotamento": str(
                        datetime.utcnow().replace(microsecond=0))}
                )
                db.session.commit()

            if (abs(roll) >= 30 or (abs(pitch - 90) >= 30)) and roll is not None and pitch is not None:
                if not prophet:
                    report(id_bin, db, apartment_ID, 90)
                current_status = 4

            if co2 >= limite_co2 and co2 is not None:
                if not prophet:
                    report(id_bin, db, apartment_ID, co2)
                current_status = 4

            return current_status

        if current_status == 3:
            if float(riempimento) >= current_threashold and riempimento is not None:
                if not prophet:
                    report(id_bin, db, apartment_ID, riempimento)
                current_status = 4

            if (abs(roll) < 30 and (abs(pitch - 90) < 30)) and roll is not None and pitch is not None:
                current_status = 1

            if co2 < limite_co2 and co2 is not None:
                current_status = 1

            return current_status

        if current_status == 4:

            if float(riempimento) < current_threashold and riempimento is not None:
                current_status = 3
                db.session.query(Bin).filter(Bin.id_bin == id_bin).update(
                    {"ultimo_svuotamento": str(
                        datetime.utcnow().replace(microsecond=0))}
                )
                db.session.commit()

            if (abs(roll) < 30 and (abs(pitch - 90) < 30)) and roll is not None and pitch is not None:
                current_status = 2

            if co2 < limite_co2 and co2 is not None:
                current_status = 2

            return current_status

    def get_organic_threashold(self, apartment_ID, id_bin):

        lat = (
            (Apartment.query.filter(Apartment.apartment_name == apartment_ID))
            .first()
            .lat
        )

        lon = (
            (Apartment.query.filter(Apartment.apartment_name == apartment_ID))
            .first()
            .lng
        )

        params = {"lat": lat, "lon": lon, "appid": self.WEATHER_KEY}

        req = requests.get(self.WEATHERE_API_URL, params=params)
        res = req.json()
        if 'error' in res:
            return 'error: ' + str(res)

        # conversione kelvin-celsius
        temp = int(res["main"]["temp"] - 272.15)
        dd_time = 0;
        
        if temp >= 20 and temp <= 25:  # medie
            dd_time = self.dd_umido["media"]

        if temp > 25 and temp <= 30:  # alte
            dd_time = self.dd_umido["alte"]

        if temp > 30:  # altissime
            dd_time = self.dd_umido["altissime"]

        timestamp = (
            Bin.query.filter(
                Bin.id_bin == id_bin).first().ultimo_svuotamento
        )

        # temperature alte + sono passo più di deltagiorni
        current_threashold = 0 if (datetime.now() - datetime.strptime(
            timestamp, "%Y-%m-%d %H:%M:%S")).days > dd_time and dd_time > 0 else self.soglie["umido"]

        return current_threashold

    def set_previsione_status(id_bin, status_previsto):
        db.session.execute(
            update(Bin)
            .where(Bin.id_bin == id_bin)
            .values({"previsione_status": status_previsto})
        )
        db.session.commit()

    def getstringstatus(status):
        if status == 1:
            return "integro, non-pieno"
        elif status == 2:
            return "integro, pieno"
        elif status == 3:
            return "manomesso, non-pieno"
        elif status == 4:
            return "manomesso, pieno"
        else:
            return "awaiting greet"

    def randomTime(rdm=True):
        # (24*60*60) = 86400 H/M/S
        # (30*12) = 360 Y/M/D
        if rdm:
            rtime = int(random.random() * 86400)
            dtime = int(random.random() * 360)

            year = 2023  # random.randrange(2022, 2023)
            month = 3
            day = random.randint(1, 31)
            hours = int(rtime / 3600)
            minutes = int((rtime - hours * 3600) / 60)
            seconds = rtime - hours * 3600 - minutes * 60
            time_string = "%s-%d-%d %02d:%02d:%02d" % (
                year,
                month,
                day,
                hours,
                minutes,
                seconds,
            )
        else:
            time_string = str(datetime.utcnow().replace(microsecond=0))
        return time_string

    def get_random_int(low: int, upper: int):
        return random.randint(low, upper)

    def get_random():
        return random.random()

    def get_limited_random(low: float, upper: float):
        return random.uniform(low, upper)

    def sa_dic2json(query):

        res = []

        for elem in query:
            elem.__dict__.pop("_sa_instance_state")
            res.append(elem.__dict__)

        return res

    def get_response(code, message, text=False):
        response = Response()
        response.status = code
        response.data = json.dumps(message) if not text else message
        response.content_type = "application/json" if not text else "text/plain"
        response.mimetype = "application/json" if not text else "text/plain"
        return response

    @property
    def get_local_time(self):
        return datetime.now()

    @property
    def get_timestamp(self):
        return datetime.timestamp(datetime.now())

    @property
    def get_post_key(self):
        return self.key
