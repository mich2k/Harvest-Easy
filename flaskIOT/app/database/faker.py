from .tables import *
  
def create_faker(db):
    
    #BinGroup
    db.session.add_all([BinGroup(), BinGroup(), BinGroup(), BinGroup()])
    
    # Admin    
    db.session.add_all([Admin(Person(username="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2000)),
                        Admin(Person(username="mario2", name="Mario", surname="Verdi", password="ilovecondomini", city="Avellino", birth_year=2000)),
                        Admin(Person(username="luigi3", name="Luigi", surname="Rossi", password="ilovecondomini", city="Moliterno", birth_year=2000))])
    
    # Apartments
    db.session.add_all([Apartment(apartment_name="Fermi", city="Modena", street="via Garibaldi", apartment_street_number=1, n_internals=155, associated_bingroup=0, associated_admin='rossi1'),
                   Apartment(apartment_name="Torri", city="Modena", street="via Garibaldi", apartment_street_number=4, n_internals=100, associated_bingroup=1, associated_admin='rossi1'),
                   Apartment(apartment_name="Cuoppo", city="Avellino", street="via Garibaldi", apartment_street_number=6, n_internals=258, associated_bingroup=2, associated_admin='mario2'),
                   Apartment(apartment_name="IDK", city="Moliterno", street="via Garibaldi", apartment_street_number=2, n_internals=50, associated_bingroup=3, associated_admin='luigi3')])
    
    #Users
    db.session.add_all([User(Person(username="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2001), "Fermi", 45),
                   User(Person(username="rossi2", name="Mario", surname="Rossi", password="ilovecondomini", city="Avellino", birth_year=2002), "Cuoppo", 67),
                   User(Person(username="rossi3", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2003), "Torri" , 78),
                   User(Person(username="rossi4", name="Mario", surname="Rossi", password="ilovecondomini", city="Avellino", birth_year=2004), "Cuoppo", 23),
                   User(Person(username="rossi5", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2005), "Fermi", 33),
                   User(Person(username="rossi6", name="Mario", surname="Rossi", password="ilovecondomini", city="Moliterno", birth_year=2006), "IDK", 12)])
    
    #Operators
    db.session.add_all([Operator(id=158), Operator(id=478), Operator(id=500)])
    
    db.session.commit()
    return True