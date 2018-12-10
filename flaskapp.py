from flask import Flask, render_template, request, url_for, abort, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os, json
from pygeocoder import Geocoder
from lyft_rides.auth import ClientCredentialGrant
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from lyft_rides.session import Session as Session2
from lyft_rides.client import LyftRidesClient
from parking_scraper import ParkMeScraper

app = Flask(__name__)
app.secret_key = 'SUPERSECRETSECRETKEY'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MONGO_URI'] = "mongodb+srv://swlabadmin:rubberduckymattress512@sw-lab-iyamn.mongodb.net/test?retryWrites=true"
mongo = PyMongo(app)
db = mongo['RideDB']

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

class User(UserMixin):

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.history = []

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)
    
    def add_history_item(self, item):
        self.history.append(item)
    
    def get_history(self):
        return self.history
    
    def query_user(cls, user)
        

@login_manager.user_loader
def load_user(id):
    #TODO! Fix this to properly load the user
    return User.get_id(id)

@app.route('/')
@app.route('/static/index.html')
@app.route('/index.html')
def index():
    return render_template('web/index.html')

@app.route('/login.html', methods = ['POST', 'GET'])
@app.route('/static/login.html', methods = ['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template('web/login.html')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        
        username = request.form['username']
        pw = request.form['password']
        

@app.route('/static/history.html')
@login_required
def history():
    # Add in more stuff about getting the user's history!
    return render_template('web/history.html')

@app.route('/result', methods=['POST'])
def result():
    if(request.method == 'POST'):
        print("REACHED HERE")
        # Do some stuff here with the variables
        source = request.form.get('source')
        destination = request.form.get('destination')

        slat,slong = geo.geocode(source).coordinates
        dlat,dlong = geo.geocode(destination).coordinates

        lots = ParkMeScraper().getLots(dlat, dlong)[:5]

        ride_estimates_uber = uber_client.get_price_estimates(slat, slong, dlat, dlong).json
        ride_estimates_lyft = lyft_client.get_cost_estimates(slat, slong, dlat, dlong).json

        return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft, lots=lots)
    else:
        print("HOW DID I DO A GET??")
        abort(403)

if __name__ == '__main__':
    app.run(debug=True)
