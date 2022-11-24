from datetime import datetime
from .__init__ import db
import json
faker_data = json.load(open('app/static/init_example_data.json', 'r'))


class Person():
    username = db.Column('username', db.String,
                         primary_key=True, nullable=False)
    name = db.Column('name', db.String)
    surname = db.Column('surname', db.String)
    password = db.Column('password', db.String)
    city = db.Column('city', db.String)
    birth_year = db.Column('birth_year', db.String)
    def __init__(self, username, name, surname, password, city, birth_year) -> None:
        self.username = username
        self.name = name
        self.surname = surname
        self.password = password
        self.city=city
        self.birth_year=birth_year

class Admin(Person, db.Model):
    __tablename__ = 'admin'
    apartments = db.relationship('Apartment', backref='admin')

    def __init__(self) -> None:
        super().__init__()


# db creation
class BinRecord(db.Model):
    __tablename__ = 'bin'
    id_record = db.Column('id_record', db.Integer, primary_key=True)
    id_bin = db.Column('id_bin', db.String)
    # 1: integro e non-pieno, 2: integro e pieno, 3: manomesso e non-pieno, 4: manomesso e pieno
    status = db.Column('status', db.Integer)
    temperature = db.Column('temperature', db.Integer, nullable=False)
    humidity = db.Column('humidity', db.Integer, nullable=False)
    co2 = db.Column('co2', db.Integer, nullable=False)
    riempimento = db.Column('livello_di_riempimento', db.Float, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),
                          nullable=False,  default=datetime.utcnow)
    

    
    # FK
    associated_bingroup = db.Column(db.Integer, db.ForeignKey('BinGroup.id'))

    
    # if no jsonObj is given, a BinRecord with fake data is created

    def __init__(self, status, jsonObj=faker_data):
        self.id_bin = jsonObj['idbin']
        self.status = status
        self.temperature = jsonObj['temperature']
        self.humidity = jsonObj['humidity']
        self.co2 = jsonObj['co2']
        self.riempimento = jsonObj['riempimento']
        self.apartment_ID = jsonObj['apartment']

    def __init__(self, id_bin, status, temperature, humidity, co2, riempimento, apartment_ID):
        self.id_bin = id_bin
        self.status = status
        self.temperature = temperature
        self.humidity = humidity
        self.co2 = co2
        self.riempimento = riempimento
        self.apartment_ID = apartment_ID


class User(Person, db.Model):
    __tablename__ = 'user'
    apartment_ID = db.Column(db.Integer, db.ForeignKey('Apartment.id'))

    def __init__(self, apartment_ID, internal_number):
        super().__init__()
        pass


class BinGroup(db.Model):
    __tablename__ = 'bingroup'
    id = db.Column('id', db.Integer, primary_key=True)
    
    
    # relationship
    
    bin_records = db.relationship('BinRecord', backref='bingroup')

    


class Apartment(db.Model):
    __tablename__ = 'apartment'
    
    # attributes
    
    id = db.Column('id', db.Integer, primary_key=True)
    apartment_name = db.Column('apartment_name', db.String, nullable=False)
    city = db.Column('city', db.String, nullable=False)
    apartment_street_number = db.Column(
        'apartment_street_number', db.Integer, nullable=False)
    street = db.Column('street', db.String, nullable=False)
    n_internals = db.Column('n_internals', db.Integer, nullable=False)
    
    # FK
    
    associated_bingroup = db.Column(db.Integer, db.ForeignKey('BinGroup.id'))
    associated_admin = db.Column(db.String, db.ForeignKey('Admin.username'))

    # relationships
    
    users = db.relationship('User', backref='apartment')
    