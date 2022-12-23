from app.database.tables import *
  
def create_faker(db):
    
    #Bin
    db.session.add_all([Bin(0, "plastica", "Fermi"), Bin(1, "umido", "Torri"), Bin(2, "carta", "Cuoppo"), Bin(3, "vetro", "IDK")])
    
    # Admin    
    db.session.add_all([Admin(Person(username="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2000)),
                        Admin(Person(username="mario2", name="Mario", surname="Verdi", password="ilovecondomini", city="Modena", birth_year=2000)),
                        Admin(Person(username="luigi3", name="Luigi", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2000))])
    
    # Apartments
    db.session.add_all([Apartment(apartment_name="Fermi", city="Modena", street="via Giuseppe Fava", lat="44.619812", lng="10.922375", apartment_street_number=49, n_internals=155, associated_bin=0, associated_admin='rossi1'),
                   Apartment(apartment_name="Torri", city="Modena", street="via Viterbo", lat="44.6229105", lng="10.9374034", apartment_street_number=90, n_internals=100, associated_bin=1, associated_admin='rossi1'),
                   Apartment(apartment_name="Cuoppo", city="Modena", street="via Ventimiglia", lat="44.6283413", lng="10.9366082", apartment_street_number=70, n_internals=258, associated_bin=2, associated_admin='mario2'),
                   Apartment(apartment_name="IDK", city="Modena", street="via Nervi", lat="44.6219696", lng="10.931554", apartment_street_number=57, n_internals=50, associated_bin=3, associated_admin='luigi3')])
    
    #Users
    db.session.add_all([User(Person(username="rossi1", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2001), "Fermi", 45),
                   User(Person(username="rossi2", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2002), "Cuoppo", 67),
                   User(Person(username="rossi3", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2003), "Torri" , 78),
                   User(Person(username="rossi4", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2004), "Cuoppo", 23),
                   User(Person(username="rossi5", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2005), "Fermi", 33),
                   User(Person(username="rossi6", name="Mario", surname="Rossi", password="ilovecondomini", city="Modena", birth_year=2006), "IDK", 12)])
    
    #Operators
    db.session.add_all([Operator(id=158), Operator(id=478), Operator(id=500)])
    
    db.session.commit()
    return True