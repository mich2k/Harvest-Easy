import requests
from app.database.tables import *
from os import getenv

TOKEN = getenv('TG_TOKEN')
URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id='.format(TOKEN)


# Filled Bin

def full_state(apartment, filling):
    #Notificare a User, Admin
    text = 'Attenzione!\nLivello di riempimento del bidone:{}'.format(str(filling))
    """"for chat_id in chat_ids:
        requests.get(URL + '{}&text={}'.format(chat_id, text))"""
    # Contattare getneighbor : via, nome dell'appartamento, città e tipologia rifiuto

# Overturned Bin


def overturn(chat_ids, coord):
    text = 'Attenzione!\nBidone rovesciato'
    for chat_id in chat_ids:
        requests.get(URL+'{}&text={}'.format(chat_id, text))

# Fired Bin


def fire(chat_ids, co2):
    text = 'Attenzione!\nRilevata elevata quantità di CO2 nel bidone({}).\nPossibile incendio in corso'.format(co2)
    for chat_id in chat_ids:
        requests.get(URL+'{}&text={}'.format(chat_id, text))
