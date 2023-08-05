from datetime import datetime
from .__init__ import db


class Person:
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column("username", db.String(20),
                         nullable=False, unique=True)

    name = db.Column("name", db.String)
    surname = db.Column("surname", db.String)
    password = db.Column("password", db.String, nullable=False)
    city = db.Column("city", db.String)
    birth_year = db.Column("birth_year", db.Integer)
    card_number = db.Column("card_number", db.String)

    def __init__(
        self,
        username: str,
        name: str,
        surname: str,
        password: str,
        city: str,
        birth_year: int,
        card_number: str
    ):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.city = city
        self.birth_year = birth_year
        self.card_number = card_number


class Admin(Person, db.Model):
    __tablename__ = "admin"

    def __init__(self, x: Person) -> None:
        super().__init__(x.username, x.name, x.surname,
                         x.password, x.city, x.birth_year, x.card_number)


class Operator(Person, db.Model):
    __tablename__ = "operator"
    id_operator = db.Column("idOperator", db.Integer)

    def __init__(self, x: Person, id: int) -> None:
        super().__init__(x.username, x.name, x.surname,
                         x.password, x.city, x.birth_year, x.card_number)
        self.id_operator = id


class User(Person, db.Model):
    __tablename__ = "user"
    internal_number = db.Column("internal_number", db.Integer)

    # FK
    apartment_ID = db.Column(
        "apartment_ID", db.String, db.ForeignKey("apartment.apartment_name"))

    def __init__(self, p: Person, apartment_ID: str, internal_number: int):
        super().__init__(p.username, p.name, p.surname,
                         p.password, p.city, p.birth_year, p.card_number)
        self.apartment_ID = apartment_ID
        self.internal_number = internal_number


# Tabelle utilizzate per mantenere le associazioni tra la chat_id del bot telegram


class UserTG(db.Model):
    __tablename__ = "idchatUser"

    id_user = db.Column("iduser", db.String, primary_key=True)
    id_chat = db.Column("idchat", db.String, default='')
    logged = db.Column("logged", db.Boolean)
    associated_user = db.Column(
        "associated_user", db.String, db.ForeignKey("user.username"))

    def __init__(self, id_user: str, id_chat: str, logged, associated_user) -> None:
        self.id_user = id_user
        self.id_chat = id_chat
        self.logged = logged
        self.associated_user = associated_user


class Superuser(Person, db.Model):
    __tablename__ = "superuser"

    def __init__(self, x: Person) -> None:
        super().__init__(x.username, x.name, x.surname,
                         x.password, x.city, x.birth_year, x.card_number)


class Bin(db.Model):
    __tablename__ = "bin"
    id_bin = db.Column("id_bin", db.Integer, primary_key=True)
    tipologia = db.Column("tipologia", db.String)
    previsione_status = db.Column(
        "previsione_status", db.String, nullable=True, default=""
    )
    ultimo_svuotamento = db.Column(
        "ultimo_svuotamento", db.String(), nullable=False, default=""
    )

    # FK
    apartment_ID = db.Column(
        "apartment_ID", db.String, db.ForeignKey("apartment.apartment_name")
    )

    def __init__(self, tipologia: str, apartment_ID: str):
        self.tipologia = tipologia
        self.apartment_ID = apartment_ID


class BinRecord(db.Model):
    __tablename__ = "binRecord"
    id_record = db.Column("id_record", db.Integer, primary_key=True)

    # 1: integro e non-pieno, 2: integro e pieno, 3: manomesso e non-pieno, 4: manomesso e pieno
    status = db.Column("status", db.Integer)
    temperature = db.Column("temperature", db.Integer, nullable=False)
    humidity = db.Column("humidity", db.Integer, nullable=False)
    riempimento = db.Column("livello_di_riempimento", db.Float, nullable=False)
    timestamp = db.Column("Timestamp", db.String, nullable=False, default=str(
        datetime.utcnow().replace(microsecond=0)))

    # FK
    associated_bin = db.Column(
        "associated_bin", db.Integer, db.ForeignKey("bin.id_bin"))

    def __init__(self, jsonObj):
        self.associated_bin = jsonObj["id_bin"]
        self.status = jsonObj["status"]
        self.temperature = jsonObj["temperature"]
        self.humidity = jsonObj["humidity"]
        self.riempimento = jsonObj["riempimento"]
        # da decommentare solo per creare il faker
        self.timestamp = jsonObj["timestamp"]


class Apartment(db.Model):
    __tablename__ = "apartment"

    apartment_name = db.Column("apartment_name", db.String, primary_key=True)
    city = db.Column("city", db.String, nullable=False)
    street = db.Column("street", db.String, nullable=False)
    lat = db.Column("lat", db.Float)
    lng = db.Column("lng", db.Float)
    apartment_street_number = db.Column(
        "apartment_street_number", db.String, nullable=False)
    n_internals = db.Column("n_internals", db.Integer, nullable=False)

    # FK
    associated_admin = db.Column(
        "associated_admin", db.String, db.ForeignKey("admin.username"))

    def __init__(
        self,
        apartment_name: str,
        city: str,
        street: str,
        lat: str,
        lng: str,
        apartment_street_number: str,
        n_internals: int,
        associated_admin: str,
    ):
        self.apartment_name = apartment_name
        self.city = city
        self.street = street
        self.lat = lat
        self.lng = lng
        self.apartment_street_number = apartment_street_number
        self.n_internals = n_internals
        self.associated_admin = associated_admin


class AlterationRecord(db.Model):
    __tablename__ = "alterationRecord"

    alteration_id = db.Column("record", db.Integer, primary_key=True)
    type_of_event = db.Column("event", db.String)
    is_notified = db.Column("is_notified", db.Boolean)
    is_solved = db.Column("is_solved", db.Boolean, default=False)
    associated_bin = db.Column(
        "associated_bin", db.Integer, db.ForeignKey("bin.id_bin"))
    timestamp = db.Column("event_timestamp", db.String, default=datetime.now())

    def __init__(self, type_of_event: str, is_notified: bool, associated_bin: int) -> None:
        self.type_of_event = type_of_event
        self.is_notified = is_notified
        self.associated_bin = associated_bin


class LeaderBoard(db.Model):
    __tablename__ = "leaderboard"

    record_id = db.Column("idrecord", db.Integer, primary_key=True)
    score = db.Column("score", db.Integer, default=0, nullable=False)
    associated_bin = db.Column(
        "associatedbin", db.String, db.ForeignKey("bin.id_bin"))
    associated_user = db.Column(
        "user", db.String, db.ForeignKey("user.username"))
    alteration_reported = db.Column(
        "alteration_reported", db.String, db.ForeignKey("alterationRecord.record"))

    def __init__(self, score: int, associated_bin: str, associated_user: str, alteration_reported: str) -> None:
        self.score = score
        self.associated_bin = associated_bin
        self.associated_user = associated_user
        self.alteration_reported = alteration_reported
