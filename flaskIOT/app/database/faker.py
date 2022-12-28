
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

def create_faker(db):
    
    #Bin
    for faker in fakers:
        db.session.add(Bin(faker))
    
    # Admin    
    db.session.add_all([Admin(Person(uid="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2000)), 
                        Admin(Person(uid="mario2", name="Mario", surname="Verdi", password="ilovecondomini", city="Avellino", birth_year=2000)),
                        Admin(Person(uid="luigi3", name="Luigi", surname="Rossi", password="ilovecondomini", city="Moliterno", birth_year=2000))])
    
    # Apartments
    db.session.add_all([Apartment(apartment_name="Fermi", city="Modena", street="via Garibaldi", apartment_street_number=1, lat='12', lng='15',n_internals=155, associated_bin=0, associated_admin='rossi1'),
                   Apartment(apartment_name="Torri", city="Modena", street="via Garibaldi", apartment_street_number=4,      lat='12', lng='15',n_internals=100, associated_bin=1, associated_admin='rossi1'),
                   Apartment(apartment_name="Cuoppo", city="Avellino", street="via Garibaldi", apartment_street_number=6,   lat='12', lng='15',n_internals=258, associated_bin=2, associated_admin='mario2'),
                   Apartment(apartment_name="IDK", city="Moliterno", street="via Garibaldi", apartment_street_number=2,     lat='12', lng='15',n_internals=50, associated_bin=3, associated_admin='luigi3')])
    
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
    
    db.session.commit()
    return True
