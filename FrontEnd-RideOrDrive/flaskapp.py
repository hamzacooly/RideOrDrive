
from flask import Flask, render_template, request, url_for, abort
import os, json
from pygeocoder import Geocoder
from lyft_rides.auth import ClientCredentialGrant
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from lyft_rides.session import Session as Session2
from lyft_rides.client import LyftRidesClient
from parking_scraper import ParkMeScraper
import urllib

app = Flask(__name__)
secrets = json.loads(open('secrets.json', 'r').read())

os.environ['GOOGLE_API_KEY'] = secrets['google_api_key']

uberServerKey = secrets['uber-server-key']
uber_session = Session(server_token=uberServerKey)
uber_client = UberRidesClient(uber_session)



googleApiKey = secrets['google_api_key']
geo = Geocoder(api_key=googleApiKey)







auth_flow = ClientCredentialGrant(
            'd-0DVSBkAukU',
            'I-yZZtV1WkY_903WKVqZEfMEls37VTCa',
            'rides.request',
            )


lyft_session = auth_flow.get_session()
lyft_client = LyftRidesClient(lyft_session)


@app.route('/')
@app.route('/static/index.html')
@app.route('/index.html')
def index():
    return render_template('web/index.html')

@app.route('/login.html')
@app.route('/static/login.html')
def login():
    return render_template('web/login.html')

@app.route('/result', methods=['POST'])
def result():
    if(request.method == 'POST'):
        print("REACHED HERE")
        # Do some stuff here with the variables
        source = request.form.get('source')
        destination = request.form.get('destination')


        sourceURL = urllib.parse.quote(source)
        destinationURL = urllib.parse.quote(destination)



        slat,slong = geo.geocode(source).coordinates
        dlat,dlong = geo.geocode(destination).coordinates

        lots = ParkMeScraper().getLots(dlat, dlong)[:5]

        ride_estimates_uber = uber_client.get_price_estimates(slat, slong, dlat, dlong).json
        ride_estimates_lyft = lyft_client.get_cost_estimates(slat, slong, dlat, dlong).json

        return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft, lots=lots, slong=slong,slat=slat,dlong=dlong,dlat=dlat, destinationURL=destinationURL,sourceURL=sourceURL)

        # return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft, lots=lots)
    else:
        print("HOW DID I DO A GET??")
        abort(403)

if __name__ == '__main__':
    app.run(debug=True)
