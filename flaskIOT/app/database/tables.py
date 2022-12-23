from datetime import datetime
from .__init__ import db

class Person():
    username = db.Column('username', db.String,
                         primary_key=True, nullable=False)  #UID=username
    name = db.Column('name', db.String)
    surname = db.Column('surname', db.String)
    password = db.Column('password', db.String)
    city = db.Column('city', db.String)
    birth_year = db.Column('birth_year', db.Integer)
    
    
    def __init__(self, username: str, name:str, surname:str, password: str, city: str, birth_year:int):
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.city=city
        self.birth_year=birth_year

class Admin(Person, db.Model):
    __tablename__ = 'admin'
    apartments = db.relationship('Apartment', backref='admin')

    def __init__(self, x: Person) -> None:
        super().__init__(x.username, x.name, x.surname, x.password, x.city, x.birth_year)

class Operator(db.Model):
    __tablename__='operator'
    id_operator = db.Column('idOperator', db.Integer, primary_key=True)
    
    def __init__(self, id: int) -> None:
        self.id_operator = id

class User(Person, db.Model):
    __tablename__ = 'user'
    apartment_ID = db.Column('apartment_ID',db.Integer, db.ForeignKey('apartment.apartment_name'))
    internal_number = db.Column('internal_number', db.Integer)
    
    def __init__(self, p: Person, apartment_ID: int, internal_number: int):
        super().__init__(p.username, p.name, p.surname, p.password, p.city, p.birth_year)
        self.apartment_ID = apartment_ID
        self.internal_number = internal_number
        
class BinRecord(db.Model):
    __tablename__ = 'binrecord'
    id_record = db.Column('id_record', db.Integer, primary_key=True)
    id_bin = db.Column('id_bin', db.String)
    
    # 1: integro e non-pieno, 2: integro e pieno, 3: manomesso e non-pieno, 4: manomesso e pieno
    status = db.Column('status', db.Integer)

    temperature = db.Column('temperature', db.Integer, nullable=False)
    humidity = db.Column('humidity', db.Integer, nullable=False)
    co2 = db.Column('co2', db.Integer, nullable=False)
    riempimento = db.Column('livello_di_riempimento', db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True), nullable=False,  default=datetime.utcnow)

    def __init__(self, status, jsonObj):
        self.id_bin = jsonObj['idbin']
        self.status = status['status']
        self.temperature = jsonObj['temperature']
        self.humidity = jsonObj['humidity']
        self.co2 = jsonObj['co2']
        self.riempimento = jsonObj['riempimento']
        

class Bin(db.Model):
    __tablename__ = 'bin'
    id_bin = db.Column('id_bin', db.String, primary_key=True)
    tipologia = db.Column('tipologia', db.String)
    apartment_ID = db.Column('apartment_ID',db.Integer, db.ForeignKey('apartment.apartment_name'))
    previsione_status = db.Column('previsione_status', db.String, nullable= True, default='')
    #timestamp = db.Column(db.DateTime(timezone=True), nullable=False,  default=datetime.utcnow) ultimo svuotamento
    
    def __init__(self, id_bin: int, tipologia: str, apartment_ID: str):
        self.id_bin = id_bin
        self.tipologia = tipologia
        self.apartment_ID = apartment_ID

class Apartment(db.Model):
    __tablename__ = 'apartment'
    
    # attributes
    apartment_name = db.Column('apartment_name', db.String, primary_key=True)
    city = db.Column('city', db.String, nullable=False)
    street = db.Column('street', db.String, nullable=False)
    lat = db.Column('lat', db.String)
    lng = db.Column('lng', db.String)
    apartment_street_number = db.Column('apartment_street_number', db.Integer, nullable=False)
    n_internals = db.Column('n_internals', db.Integer, nullable=False)
    
    # FK
    associated_bin = db.Column(db.Integer, db.ForeignKey('bin.id_bin'))
    associated_admin = db.Column(db.String, db.ForeignKey('admin.username'))
    

    # relationships
    users = db.relationship('User', backref='apartment')
    
    def __init__(self, apartment_name: str, city: str, street: str, lat: str, lng: str,
                apartment_street_number: int, n_internals: int, associated_bin: int, associated_admin: str):
        self.apartment_name = apartment_name
        self.city = city
        self.street = street
        self.lat = lat
        self.lng = lng
        self.apartment_street_number = apartment_street_number
        self.n_internals = n_internals
        self.associated_bin = associated_bin
        self.associated_admin = associated_admin

    