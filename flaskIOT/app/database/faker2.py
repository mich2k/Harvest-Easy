from .tables import *
from ..utils import utils

timestamps = utils.Utils.randomTime()

fakers = [{'idbin':1,'tipologia':'carta',    'ultimo_svuotamento':timestamps[0], 'apartment_ID':'Fermi'},
          {'idbin':2,'tipologia':'plastica', 'ultimo_svuotamento':timestamps[1], 'apartment_ID':'Fermi'},
          {'idbin':3,'tipologia':'vetro',    'ultimo_svuotamento':timestamps[2], 'apartment_ID':'Fermi'},
          {'idbin':4,'tipologia':'carta',    'ultimo_svuotamento':timestamps[3], 'apartment_ID':'Torri'},
          {'idbin':5,'tipologia':'plastica', 'ultimo_svuotamento':timestamps[4], 'apartment_ID':'Torri'},
          {'idbin':6,'tipologia':'umido',    'ultimo_svuotamento':timestamps[5], 'apartment_ID':'Cuoppo'},
          {'idbin':7,'tipologia':'plastica', 'ultimo_svuotamento':timestamps[6], 'apartment_ID':'Cuoppo'},
          {'idbin':8,'tipologia':'carta',    'ultimo_svuotamento':timestamps[7], 'apartment_ID':'Cuoppo'}]

faker_record=[{"status": 2, "temperature": 26, "humidity": 49, "co2": 80, "riempimento": 20, "idbin": 5},
              {"status": 2, "temperature": 26, "humidity": 49, "co2": 80, "riempimento": 20, "idbin": 1},
              {"status": 2, "temperature": 26, "humidity": 49, "co2": 80, "riempimento": 20, "idbin": 2},
              {"status": 2, "temperature": 26, "humidity": 49, "co2": 80, "riempimento": 20, "idbin": 3},
              {"status": 2, "temperature": 26, "humidity": 49, "co2": 80, "riempimento": 20, "idbin": 4},
              {"status": 2, "temperature": 26, "humidity": 49, "co2": 80, "riempimento": 20, "idbin": 6}]

def create_faker(db):
    
    #Bin
    for faker in fakers:
        db.session.add(Bin(faker))
        
    #BinRecord
    for faker in faker_record:
        db.session.add(BinRecord(faker))
    
    # Admin    
    db.session.add_all([Admin(Person(uid="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2000)),
                        Admin(Person(uid="mario2", name="Mario", surname="Verdi", password="ilovecondomini", city="Modena", birth_year=2000)),
                        Admin(Person(uid="luigi3", name="Luigi", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2000))])
    
    # Apartments
    db.session.add_all([Apartment(apartment_name="Fermi", city="Modena", street="via Giuseppe Fava", apartment_street_number=49, lat=44.6194014, lng=10.9217465,n_internals=155, associated_admin='rossi1'),
                   Apartment(apartment_name="Torri", city="Modena", street="via Viterbo", apartment_street_number=90, lat=44.6229105, lng=10.9374034,n_internals=100, associated_admin='rossi1'),
                   Apartment(apartment_name="Cuoppo", city="Modena", street="via Nervi", apartment_street_number=57, lat=44.6219696, lng=10.931554,n_internals=258, associated_admin='mario2'),
                   Apartment(apartment_name="IDK", city="Modena", street="via Cividale", apartment_street_number=80, lat=44.6270617, lng=10.9183277,n_internals=50, associated_admin='luigi3')])
    
    #Users
    db.session.add_all([User(Person(uid="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2001), apartment_ID="Fermi", internal_number=45),
                   User(Person(uid="rossi2", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2002), apartment_ID="Cuoppo", internal_number=67),
                   User(Person(uid="rossi3", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2003), apartment_ID="Torri" , internal_number=78),
                   User(Person(uid="rossi4", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2004), apartment_ID="Cuoppo", internal_number=23),
                   User(Person(uid="rossi5", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2005), apartment_ID="Fermi", internal_number=33),
                   User(Person(uid="rossi6", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2006), apartment_ID="IDK", internal_number=12)])
    
    #Operators
    db.session.add_all([Operator(Person(uid="rossi8", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2004),id=158), 
                        Operator(Person(uid="rossi10", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2004),id=478), 
                        Operator(Person(uid="rossi11", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2004),id=500)])
    
    db.session.commit()
    return True