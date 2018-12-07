from flask import Flask, render_template, request, url_for, abort
import os, json
import geocoder
from lyft_rides.auth import ClientCredentialGrant
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from lyft_rides.session import Session as Session2
from lyft_rides.client import LyftRidesClient

app = Flask(__name__)
secrets = json.loads(open('secrets.json', 'r').read())

os.environ['GOOGLE_API_KEY'] = secrets['google_api_key']

uberServerKey = secrets['uber-server-key']
uber_session = Session(server_token=uberServerKey)
uber_client = UberRidesClient(uber_session)

#lyftServerKey = secrets['lyft-server-key']

auth_flow = ClientCredentialGrant(
            'd-0DVSBkAukU',
            'I-yZZtV1WkY_903WKVqZEfMEls37VTCa',
            'rides.request',
            )
lyft_session = auth_flow.get_session()
lyft_client = LyftRidesClient(lyft_session)


@app.route('/')
def index():
    return render_template('web/index.html')

@app.route('/result', methods=['POST'])
def result():
    if(request.method == 'POST'):
        print("REACHED HERE")
        # Do some stuff here with the variables
        source = request.form.get('source')
        destination = request.form.get('destination')
        slatlong = geocoder.google(source, method="reverse").latlng
        dlatlong = geocoder.google(destination, method="reverse").latlng
        slat = slatlong[0]
        slong = slatlong[1]
        dlat = dlatlong[0]
        dlong = dlatlong[1]

        ride_estimates_uber = uber_client.get_price_estimates(slat, slong, dlat, dlong).json
        ride_estimates_lyft = lyft_client.get_cost_estimates(slat, slong, dlat, dlong).json

        return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft)
    else:
        print("HOW DID I DO A GET??")
        abort(403)

if __name__ == '__main__':
    app.run(debug=True)