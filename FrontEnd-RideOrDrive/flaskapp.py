from flask import Flask, render_template, request, url_for, abort, redirect, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
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
from weather_scraper import WeatherScraper
import urllib

app = Flask(__name__)
app.secret_key = 'SUPERSECRETSECRETKEY'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

app.config['MONGO_URI'] = "mongodb+srv://swlabadmin:rubberduckymattress512@sw-lab-iyamn.mongodb.net/RideDB?retryWrites=true"
mongo = PyMongo(app)
appDB = mongo.db

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

    def __init__(self, username, password, history):
        self.username = username
        self.set_password(password)
        self.history = history

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def add_history_item(self, item):
        self.history.append(item)
        appDB.users[self.username]['history'].insert(item)

    def get_history(self):
        return self.history

    @staticmethod
    def query_user(id):
        user = appDB.users.find_one({'_id': id})
        if user:
            return User(user._id, user.password, user.history)
        else:
            return None

@login_manager.user_loader
def load_user(id):
    return User.query_user(id)

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
        user = appDB.users.find_one({'_id': username})
        if user:
            myuser = User(user._id, user.password, user.history)
            if myuser.check_password(pw):
                login_user(myuser)
                redirect(url_for(index))
            else:
                flash("Incorrect password, please try again")
        else:
            myuser = User(username, pw, [])
            appDB.users.insert({"_id": myuser.username, \
                                "password": myuser.pw_hash, \
                                "history": []})

@app.route('/static/history.html')
@login_required
def history():
    # Add in more stuff about getting the user's history!
    return render_template('web/history.html')

@app.route('/result', methods=['POST'])
def result():
    if(request.method == 'POST'):
        # Do some stuff here with the variables
        source = request.form.get('source')
        destination = request.form.get('destination')


        sourceURL = urllib.parse.quote(source)
        destinationURL = urllib.parse.quote(destination)



        slat,slong = geo.geocode(source).coordinates
        dlat,dlong = geo.geocode(destination).coordinates
        dregion = geo.reverse_geocode(dlat,dlong).county

        lots = ParkMeScraper().getLots(dlat, dlong)[:5]


        weather = WeatherScraper().get_weather(dlat,dlong)
        print(weather)

        try:
            ride_estimates_uber = uber_client.get_price_estimates(slat, slong, dlat, dlong).json
        except:
            ride_estimates_uber = {}

        try:
            ride_estimates_lyft = lyft_client.get_cost_estimates(slat, slong, dlat, dlong).json
        except:
            ride_estimates_lyft = {}


        lotsMarkers = []
        for lot in lots:
            entry={}
            entry['name']= lot['name']
            mlat,mlong = geo.geocode(lot['address']+" "+dregion).coordinates
            entry['mlat'] = mlat
            entry['mlong'] = mlong
            lotsMarkers.append(entry)




        return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft, lots=lots, weather=weather, slong=slong,slat=slat,dlong=dlong,dlat=dlat, destinationURL=destinationURL,sourceURL=sourceURL, lotsMarkers=lotsMarkers)

        # return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft, lots=lots)
    else:
        print("HOW DID I DO A GET??")
        abort(403)

if __name__ == '__main__':
    app.run(debug=True)
