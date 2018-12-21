from flask import Flask
import os, json
from pygeocoder import Geocoder
from lyft_rides.auth import ClientCredentialGrant
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from lyft_rides.client import LyftRidesClient
from parking_scraper import ParkMeScraper
from weather_scraper import WeatherScraper

app = Flask(__name__)
app.secret_key = 'SUPERSECRETSECRETKEY'
app.config['MONGO_URI'] = "mongodb+srv://swlabadmin:rubberduckymattress512@sw-lab-iyamn.mongodb.net/RideDB?retryWrites=true"

secrets = json.loads(open('secrets.json', 'r').read())
os.environ['GOOGLE_API_KEY'] = secrets['google_api_key']

uberServerKey = secrets['uber-server-key']
uber_session = Session(server_token=uberServerKey)
uber_client = UberRidesClient(uber_session)

googleApiKey = secrets['google_api_key']
geo = Geocoder(api_key=googleApiKey)
pms = ParkMeScraper()
ws = WeatherScraper()

auth_flow = ClientCredentialGrant(
            'd-0DVSBkAukU',
            'I-yZZtV1WkY_903WKVqZEfMEls37VTCa',
            'rides.request',
            )

lyft_session = auth_flow.get_session()
lyft_client = LyftRidesClient(lyft_session)

from views import *

if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'),debug=False)
