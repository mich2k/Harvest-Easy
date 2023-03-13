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
        "apartment_ID": "Trento",
    },
    {
        "idbin": 7,
        "tipologia": "plastica",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Trento",
    },
    {
        "idbin": 8,
        "tipologia": "carta",
        "ultimo_svuotamento": utils.Utils.randomTime(),
        "apartment_ID": "Viali",
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
                street="via Giuseppe Verdi",
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
                apartment_name="Trento",
                city="Modena",
                street="via Nervi",
                apartment_street_number='57',
                lat=44.6219696,
                lng=10.931554,
                n_internals=258,
                associated_admin="mario2",
            ),
            Apartment(
                apartment_name="Viali",
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
                    username="mick",
                    name="Michele",
                    surname="Giarletta",
                    password=generate_password("michelegiarletta"),
                    city="Modena",
                    birth_year=2001,
                    card_number="d3370a6"
                ),
                "Fermi",
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
            )
        ]
    )

    # Operators
    db.session.add_all(
        [
            Operator(
                Person(
                    username="marco",
                    name="Marco",
                    surname="Verdi",
                    password=generate_password("marcoverdi"),
                    city="Modena",
                    birth_year=2000,
                    card_number="d337048"
                ),
                id=158,
            )
        ]
    )

    # Telegram profiles
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
