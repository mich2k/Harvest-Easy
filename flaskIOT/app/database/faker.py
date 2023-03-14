from .tables import *
from ..utils import utils
from .record_faker import faker_instances
from app.login.login import generate_password

fakers = [
    {
        "idbin": 1,
        "tipologia": "carta",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Fermi",
    },
    {
        "idbin": 2,
        "tipologia": "plastica",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Fermi",
    },
    {
        "idbin": 3,
        "tipologia": "vetro",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Fermi",
    },
    {
        "idbin": 4,
        "tipologia": "carta",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Torri",
    },
    {
        "idbin": 5,
        "tipologia": "plastica",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Torri",
    },
    {
        "idbin": 6,
        "tipologia": "umido",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Cuoppo",
    },
    {
        "idbin": 7,
        "tipologia": "plastica",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Cuoppo",
    },
    {
        "idbin": 8,
        "tipologia": "carta",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "IDK",
    },
]


def create_faker(db):

    # Bin
    for faker in fakers:
        db.session.add(
            Bin(faker['tipologia'], apartment_ID=faker['apartment_ID']))

    # Admin
    db.session.add_all(
        [
            Admin(
                Person(
                    username="rossi1",
                    name="Mario",
                    surname="Rossi",
                    password=generate_password("mariorossi"),
                    city="Modena",
                    birth_year=2000,
                    card_number="d3370a8"
                )
            ),
            Admin(
                Person(
                    username="mario2",
                    name="Mario",
                    surname="Verdi",
                    password=generate_password("marioverdi"),
                    city="Avellino",
                    birth_year=2000,
                    card_number="d3370a9"
                )
            ),
            Admin(
                Person(
                    username="luigi3",
                    name="Luigi",
                    surname="Rossi",
                    password=generate_password("luigirossi"),
                    city="Moliterno",
                    birth_year=2000,
                    card_number="d3370a0"
                )
            ),
        ]
    )

    # Apartments
    db.session.add_all(
        [
            Apartment(
                apartment_name="Fermi",
                city="Modena",
                street="via Giuseppe Fava",
                apartment_street_number='49',
                lat=44.6194014,
                lng=10.9217465,
                n_internals=155,
                associated_admin="rossi1",
            ),
            Apartment(
                apartment_name="Torri",
                city="Modena",
                street="via Viterbo",
                apartment_street_number='90',
                lat=44.6229105,
                lng=10.9374034,
                n_internals=100,
                associated_admin="rossi1",
            ),
            Apartment(
                apartment_name="Cuoppo",
                city="Modena",
                street="via Nervi",
                apartment_street_number='57',
                lat=44.6219696,
                lng=10.931554,
                n_internals=258,
                associated_admin="mario2",
            ),
            Apartment(
                apartment_name="IDK",
                city="Modena",
                street="via Cividale",
                apartment_street_number='80',
                lat=44.6280877,
                lng=10.9166076,
                n_internals=50,
                associated_admin="luigi3",
            ),
        ]
    )

    # Users
    db.session.add_all(
        [
            User(
                Person(
                    username="vinz",
                    name="Vincenzo",
                    surname="Lapadula",
                    password=generate_password("vincenzolapadula"),
                    city="Modena",
                    birth_year=2001,
                    card_number="d3370a5"
                ),
                "Fermi",
                45,
            ),
            User(
                Person(
                    username="chad",
                    name="Michele",
                    surname="Giarletta",
                    password=generate_password("michelegiarletta"),
                    city="Avellino",
                    birth_year=2002,
                    card_number="d3370a6"
                ),
                "Cuoppo",
                67,
            ),
            User(
                Person(
                    username="ale",
                    name="Alessia",
                    surname="Saporita",
                    password=generate_password("alessiasaporita"),
                    city="Modena",
                    birth_year=2000,
                    card_number="d3370a8"
                ),
                "Fermi",
                45,
            ),
            User(
                Person(
                    username="nenna",
                    name="Elena",
                    surname="Berselli",
                    password=generate_password("elenaberselli"),
                    city="Modena",
                    birth_year=2000,
                    card_number="d3370b8"
                ),
                "Torri",
                78,
            ),
            User(
                Person(
                    username="lollo",
                    name="Lorenzo",
                    surname="Venturelli",
                    password=generate_password("lorenzoventurelli"),
                    city="Avellino",
                    birth_year=2004,
                    card_number="d337018"
                ),
                "Cuoppo",
                23,
            ),
            User(
                Person(
                    username="abby",
                    name="Abeer",
                    surname="Jelali",
                    password=generate_password("abeerjelali"),
                    city="Modena",
                    birth_year=2005,
                    card_number="d337028"
                ),
                "Fermi",
                33,
            ),
            User(
                Person(
                    username="turro",
                    name="Alessio",
                    surname="Turrini",
                    password=generate_password("alessioturrini"),
                    city="Moliterno",
                    birth_year=2006,
                    card_number="d337038"
                ),
                "IDK",
                12,
            ),
        ]
    )

    # Operators
    db.session.add_all(
        [
            Operator(
                Person(
                    username="mattia",
                    name="Mattia",
                    surname="Gualtieri",
                    password=generate_password("mattiagualtieri"),
                    city="Avellino",
                    birth_year=2004,
                    card_number="d337048"
                ),
                id=158,
            ),
            Operator(
                Person(
                    username="guido",
                    name="Guido",
                    surname="Benevelli",
                    password=generate_password("guidobenevelli"),
                    city="Modena",
                    birth_year=2004,
                    card_number="d3375a8",
                ),
                id=478,
            ),
            Operator(
                Person(
                    username="rasta",
                    name="Gabriele",
                    surname="Rastelli",
                    password=generate_password("gabrielerastelli"),
                    city="Avellino",
                    birth_year=2004,
                    card_number="d337068"
                ),
                id=500,
            )
        ]
    )

    # Mich & Vinz Telegram profiles
    db.session.add_all(
        [
            UserTG("@vinz20110", "",
                   logged=False, associated_user="vinz"),
            UserTG("@mich2k", "", logged=False, associated_user="chad"),
        ]
    )

    # BinRecords
    for i in range(50):
        db.session.add(BinRecord(faker_instances()))

    db.session.commit()
    return True
