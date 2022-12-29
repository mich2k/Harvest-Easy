
from .tables import *
from ..utils import utils
from .record_faker import faker_instances
import random

fakers = [{'idbin':1,'tipologia':'carta',    'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Fermi'},
          {'idbin':2,'tipologia':'plastica', 'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Fermi'},
          {'idbin':3,'tipologia':'vetro',    'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Fermi'},
          {'idbin':4,'tipologia':'carta',    'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Torri'},
          {'idbin':5,'tipologia':'plastica', 'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Torri'},
          {'idbin':6,'tipologia':'umido',    'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Cuoppo'},
          {'idbin':7,'tipologia':'plastica', 'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Cuoppo'},
          {'idbin':8,'tipologia':'carta',    'ultimo_svuotamento':utils.Utils.randomTime(), 'apartment_ID':'Cuoppo'}]

def create_faker(db):
    
    #Bin
    for faker in fakers:
        db.session.add(Bin(faker))
    
    # Admin    
    db.session.add_all([Admin(Person(uid="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2000)), 
                        Admin(Person(uid="mario2", name="Mario", surname="Verdi", password="ilovecondomini", city="Avellino", birth_year=2000)),
                        Admin(Person(uid="luigi3", name="Luigi", surname="Rossi", password="ilovecondomini", city="Moliterno", birth_year=2000))])
    
    # Apartments
    db.session.add_all([Apartment(apartment_name="Fermi", city="Modena", street="via Giuseppe Fava", apartment_street_number=49, lat=44.619401, lng=10.921746,n_internals=155, associated_admin='rossi1'),
                   Apartment(apartment_name="Torri", city="Modena", street="via Viterbo", apartment_street_number=90, lat=44.622911, lng=10.937403,n_internals=100, associated_admin='rossi1'),
                   Apartment(apartment_name="Cuoppo", city="Modena", street="via Nervi", apartment_street_number=57, lat=44.621969, lng=10.931554,n_internals=258, associated_admin='mario2'),
                   Apartment(apartment_name="IDK", city="Modena", street="via Cividale", apartment_street_number=80, lat=44.627061, lng=10.918327,n_internals=50, associated_admin='luigi3')])
    
    #Users
    db.session.add_all([User(Person(uid="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2001), "Fermi", 45),
                   User(Person(uid="rossi2", name="Mario", surname="Rossi", password="ilovecondomini", city="Avellino", birth_year=2002), "Cuoppo", 67),
                   User(Person(uid="rossi3", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2003), "Torri" , 78),
                   User(Person(uid="rossi4", name="Mario", surname="Rossi", password="ilovecondomini", city="Avellino", birth_year=2004), "Cuoppo", 23),
                   User(Person(uid="rossi5", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2005), "Fermi", 33),
                   User(Person(uid="rossi6", name="Mario", surname="Rossi", password="ilovecondomini", city="Moliterno", birth_year=2006), "IDK", 12)])
    
    #Operators
    db.session.add_all([Operator(Person(uid="rossi8", name="Mario", surname="Rossi", password="ilovecondomini", city="Avellino", birth_year=2004),id=158), 
                        Operator(Person(uid="rossi10", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2004),id=478), 
                        Operator(Person(uid="rossi11", name="Mario", surname="Rossi", password="ilovecondomini", city="Avellino", birth_year=2004),id=500)])
    
    
    #BinRecords
    for i in range(90):
        db.session.add(BinRecord(faker_instances()))
        
    db.session.commit()
    return True
