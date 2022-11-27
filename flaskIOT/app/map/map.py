from flask import Blueprint
import requests
from os import getenv

HERE_API_KEY = getenv('HERE_KEY')

map_blueprint = Blueprint('map', __name__, template_folder='templates')
@map_blueprint.route('/')
def main():
    return '<h1>Map</h1>'


# Simplest way to get the lat, long of any address.

# Using Python requests and the Google Maps Geocoding API.

import requests
@map_blueprint.route('/')
def main(): 

HERE_API_URL = f'GET https://geocode.search.hereapi.com/v1/geocode?q=240+Washington+St.%2C+Boston&apiKey={HERE_API_KEY}'

params = {
    'address': 'oshiwara industerial center goregaon west mumbai',
    'sensor': 'false',
    'region': 'india'
}

# Do the request and get the response data
req = requests.get(GOOGLE_MAPS_API_URL, params=params)
res = req.json()

# Use the first result
result = res['results'][0]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))

# Result => Link Rd, Best Nagar, Goregaon West, Mumbai, Maharashtra 400104, India. (lat, lng) = (19.1528967, 72.8371262)