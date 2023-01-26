from datetime import datetime
from .__init__ import db
#from flasky import bcrypt


class Person:
    uid = db.Column("uid", db.String, primary_key=True, nullable=False)
    name = db.Column("name", db.String)
    surname = db.Column("surname", db.String)
    password = db.Column("password", db.String)
    city = db.Column("city", db.String)
    birth_year = db.Column("birth_year", db.Integer)

    def __init__(
        self,
        uid: str,
        name: str,
        surname: str,
        password: str,
        city: str,
        birth_year: int,
    ):
        self.uid = uid
        self.name = name
        self.surname = surname
        #self.password = bcrypt.generate_password_hash(password)
        self.city = city
        self.birth_year = birth_year


class UserTG:
    id_user = db.Column("iduser", db.String, primary_key=True)
    logged = db.Column("logged", db.Boolean)

    def __init__(self, id_user: str, logged) -> None:
        self.id_user = id_user
        self.logged = logged


class Admin(Person, db.Model):
    __tablename__ = "admin"

    def __init__(self, x: Person) -> None:
        super().__init__(x.uid, x.name, x.surname, x.password, x.city, x.birth_year)


class Operator(Person, db.Model):
    __tablename__ = "operator"
    id_operator = db.Column("idOperator", db.Integer)

    def __init__(self, x: Person, id: int) -> None:
        super().__init__(x.uid, x.name, x.surname, x.password, x.city, x.birth_year)
        self.id_operator = id


class User(Person, db.Model):
    __tablename__ = "user"
    internal_number = db.Column("internal_number", db.Integer)
    # FK
    apartment_ID = db.Column(
        "apartment_ID", db.Integer, db.ForeignKey("apartment.apartment_name")
    )

    def __init__(self, p: Person, apartment_ID: int, internal_number: int):
        super().__init__(p.uid, p.name, p.surname, p.password, p.city, p.birth_year)
        self.apartment_ID = apartment_ID
        self.internal_number = internal_number


class Superuser(Person, db.Model):
    __tablename__ = "superuser"

    def __init__(self, x: Person) -> None:
        super().__init__(x.uid, x.name, x.surname, x.password, x.city, x.birth_year)


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
        "apartment_ID", db.Integer, db.ForeignKey("apartment.apartment_name")
    )

    def __init__(self, jsonObj):
        self.id_bin = jsonObj["idbin"]
        self.tipologia = jsonObj["tipologia"]
        self.apartment_ID = jsonObj["apartment_ID"]

        # da decommentare solo per il faker
        self.ultimo_svuotamento = jsonObj["ultimo_svuotamento"]


class BinRecord(db.Model):
    __tablename__ = "binRecord"
    id_record = db.Column("id_record", db.Integer, primary_key=True)

    # 1: integro e non-pieno, 2: integro e pieno, 3: manomesso e non-pieno, 4: manomesso e pieno
    status = db.Column("status", db.Integer)
    temperature = db.Column("temperature", db.Integer, nullable=False)
    humidity = db.Column("humidity", db.Integer, nullable=False)
    riempimento = db.Column("livello_di_riempimento", db.Float, nullable=False)
    timestamp = db.Column(
        "Timestamp",
        db.String,
        nullable=False,
        default=str(datetime.utcnow().replace(microsecond=0)),
    )
    # FK
    associated_bin = db.Column(
        "associated_bin", db.Integer, db.ForeignKey("bin.id_bin")
    )

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
        "apartment_street_number", db.Integer, nullable=False
    )
    n_internals = db.Column("n_internals", db.Integer, nullable=False)

    # FK
    associated_admin = db.Column(
        "associated_admin", db.String, db.ForeignKey("admin.uid")
    )

    def __init__(
        self,
        apartment_name: str,
        city: str,
        street: str,
        lat: str,
        lng: str,
        apartment_street_number: int,
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


# Tabelle utilizzate per mantenere le associazioni tra la chat_id del bot telegram


class TelegramIDChatUser(UserTG, db.Model):
    __tablename__ = "idchatUser"

    associated_user = db.Column("associated_user", db.String, db.ForeignKey("user.uid"))

    def __init__(self, user: UserTG, associated_user: str) -> None:
        super().__init__(user.id_user, user.logged)
        self.associated_user = associated_user


class LeaderBoard(db.Model):
    __tablename__ = "leaderboard"

    record_id = db.Column("idrecord", db.Integer, primary_key=True)
    score = db.Column("score", db.Integer, default=0)
    associated_bin = db.Column("associatedbin", db.String, db.ForeignKey("bin.id_bin"))
    associated_user = db.Column("user", db.String, db.ForeignKey("user.uid"))
    alteration_solved = db.Column("alteration_solved", db.String, default="")

    def __init__(self, score, associated_bin, associated_user) -> None:
        self.score = score
        self.associated_bin = associated_bin
        self.associated_user = associated_user


class AlterationRecord(db.Model):
    __tablename__ = "alterationRecord"

    alteration_id = db.Column("record", db.Integer, primary_key=True)
    type_of_event = db.Column("event", db.String)
    is_notified = db.Column(
        "is_notified",
        db.Boolean,
    )
    is_solved = db.Column("is_solved", db.Boolean, default=False)
    associated_bin = db.Column("associated_bin", db.String, db.ForeignKey("bin.id_bin"))
    timestamp = db.Column("event_timestamp", db.String, default=datetime.now())

    def __init__(self, type_of_event, is_notified, associated_bin) -> None:
        self.type_of_event = type_of_event
        self.is_notified = is_notified
        self.associated_bin = associated_bin
