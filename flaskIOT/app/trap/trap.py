import requests
from app.database.tables import *
from os import getenv

TOKEN = getenv('TG_TOKEN')
ids = getenv('IDs').split(', ')
URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id='.format(TOKEN)

def trap(text):
    return requests.get(URL+'{}&text= {}'.format(ids[0], text)).json()

#Filled Bin 
def full_state(filling):
    pass    

#Overturned Bin
def overturn(coord):
    pass

#Fired Bin
def fire(co2):
    pass