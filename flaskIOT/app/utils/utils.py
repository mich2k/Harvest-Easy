from datetime import datetime
from flask import Response
from os import getenv
from ..database.tables import *
from ..trap.trap import *
import random, requests


class Utils:

    HERE_API_KEY = getenv("HERE_KEY")
    WEATHER_KEY = getenv("WEATHER_KEY")

    def __init__(self):
        # self.key = getenv['POST_SECRET_KEY']
        self.key = "maybesupersecretkey"

    def calcolastatus(self, id_bin, riempimento, roll, pitch, co2):

        soglie = {
            "plastica": 0.9,
            "carta": 0.9,
            "vetro": 0.8,
            "umido": 0.7,
        }  # soglie fisse

        # soglia dinamica per l'organico in base alla temperatura
        dd_umido = {"medie": 5, "alte": 3, "altissime": 2}

        limite_co2 = 2000  # 2000ppm
        status_attuale = 1  # default del primo record del bidone

        bin_attuale = BinRecord.query.filter(BinRecord.associated_bin == id_bin)

        if bin_attuale.count():
            status_attuale = (
                BinRecord.query.filter(BinRecord.associated_bin == id_bin)
                .order_by(BinRecord.timestamp.desc())
                .first()
            ).status

        tipologia = (Bin.query.filter(Bin.id_bin == id_bin)).first().tipologia
        apartment_ID = (Bin.query.filter(Bin.id_bin == id_bin)).first().apartment_ID
        soglia_attuale = 0

        if tipologia == "umido":
            now = datetime.now()
            mese = now.month
            if mese >= 4 and mese <= 10:  # mesi caldi
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

                WEATHERE_API_URL = f"https://api.openweathermap.org/data/2.5/weather"
                params = {"lat": lat, "lon": lon, "appid": self.WEATHER_KEY}

                req = requests.get(WEATHERE_API_URL, params=params)
                res = req.json()
                # conversione kelvin-celsius
                temp = int(res["main"]["temp"] - 272.15)
                dd_time = 0

                if temp >= 20 and temp <= 25:  # medie
                    dd_time = dd_umido["media"]

                if temp > 25 and temp <= 30:  # alte
                    dd_time = dd_umido["alte"]

                if temp > 30:  # altissime
                    dd_time = dd_umido["altissime"]

                timestamp = (
                    Bin.query.filter(Bin.id_bin == id_bin).first().ultimo_svuotamento
                )
                last_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                now = datetime.now()

                # temperature alte + sono passo più di deltagiorni
                if (now - last_date).days > dd_time and dd_time > 0:
                    soglia_attuale = 0
                else:
                    soglia_attuale = soglie["umido"]
            else:
                soglia_attuale = soglie["umido"]
        elif tipologia == "plastica":
            soglia_attuale = soglie["plastica"]
        elif tipologia == "carta":
            soglia_attuale = soglie["carta"]
        elif tipologia == "vetro":
            soglia_attuale = soglie["vetro"]

        """ 1: integro e non-pieno, 
            2: integro e pieno, 
            3: manomesso e non-pieno, 
            4: manomesso e pieno
        """

        # TODO rendere più fine
        if riempimento != None:
            # passaggio da pieno a non pieno e viceversa
            if status_attuale == 1 and float(riempimento) >= soglia_attuale:
                full_state(id_bin, apartment_ID, riempimento)
                status_attuale = 2

            if status_attuale == 3 and float(riempimento) >= soglia_attuale:
                full_state(id_bin, apartment_ID, riempimento)
                status_attuale = 4

            if status_attuale == 2 and float(riempimento) < soglia_attuale:
                status_attuale = 1
                db.session.query(Bin).filter(Bin.id_bin == id_bin).update(
                    {"ultimo_svuotamento": datetime.now()}
                )
                db.session.commit()

            if status_attuale == 4 and float(riempimento) < soglia_attuale:
                status_attuale = 3
                db.session.query(Bin).filter(Bin.id_bin == id_bin).update(
                    {"ultimo_svuotamento": datetime.now()}
                )
                db.session.commit()

        # passaggio da accappottato a dritto e viceversa
        if roll != None and pitch != None:
            if status_attuale == 3 and (abs(roll) < 30 and (abs(pitch - 90) < 30)):
                status_attuale = 1

            if status_attuale == 1 and (abs(roll) >= 30 or (abs(pitch - 90) >= 30)):
                overturn(id_bin, apartment_ID, 90)
                status_attuale = 3

            if status_attuale == 4 and (abs(roll) < 30 and (abs(pitch - 90) < 30)):
                status_attuale = 2

            if status_attuale == 2 and (abs(roll) >= 30 or (abs(pitch - 90) >= 30)):
                overturn(id_bin, apartment_ID, 90)
                status_attuale = 4
        if co2 != None:
            # Caso in cui nel bidone ci dovesse essere un incendio
            if status_attuale == 3 and co2 < limite_co2:
                status_attuale = 1

            if status_attuale == 1 and co2 >= limite_co2:
                fire(id_bin, apartment_ID, co2)
                status_attuale = 3

            if status_attuale == 4 and co2 < limite_co2:
                status_attuale = 2

            if status_attuale == 2 and co2 >= limite_co2:
                fire(id_bin, apartment_ID, co2)
                status_attuale = 4

        return status_attuale

    def set_previsione_status(id_bin, status_previsto):
        db.session.query(Bin).filter(Bin.id_bin == id_bin).update(
            {"previsione_status": status_previsto}
        )
        db.session.commit()

    def getstringstatus(status):
        if status == 1:
            return "integro e non-pieno"
        elif status == 2:
            return "integro e pieno"
        elif status == 3:
            return "manomesso e non-pieno"
        elif status == 4:
            return "manomesso e pieno"
        else:
            return "Error"

    def randomTime(rdm=True):
        # (24*60*60) = 86400 H/M/S
        # (30*12) = 360 Y/M/D
        if rdm:
            rtime = int(random.random() * 86400)
            dtime = int(random.random() * 360)

            year = 2022 #random.randrange(2022, 2023)
            month = int(dtime / 30) if int(dtime / 30) != 0 else int(dtime / 30) + 1
            day = int(dtime / 12) if int(dtime / 12) != 0 else int(dtime / 12) + 1
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

    def sa_dic2json(query):

        res = []

        for elem in query:
            elem.__dict__.pop("_sa_instance_state")
            res.append(elem.__dict__)

        return res

    def get_response(code, message):
        response = Response()
        response.status = code
        response.data = message
        response.content_type = "text/plain"
        response.mimetype = "text/plain"
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
