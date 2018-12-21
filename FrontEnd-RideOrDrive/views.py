from flask import render_template, request, redirect, flash, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from flaskapp import app, uber_client, lyft_client, geo, pms, ws
from auth import login_manager, User, check_password
from db import appDB
import urllib, time

@app.route('/static/index.html')
@app.route('/index.html')
@app.route('/')
def index():
    return render_template('web/index.html')

@app.route('/login.html', methods = ['POST', 'GET'])
@app.route('/static/login.html', methods = ['POST', 'GET'])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        return render_template('web/login.html')
    else:
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        username = request.form['username']
        pw = request.form['password']
        user = appDB.users.find_one({'_id': username})
        if user:
            myuser = User.query_user(user['_id'])
            if check_password(myuser.pw_hash, pw):
                login_user(myuser)
                return redirect(url_for('index'))
            else:
                flash("Incorrect username/password, please try again")
                return render_template('web/login.html')
        else:
            pw_hash = generate_password_hash(pw)
            myuser = User(username, pw_hash, [])
            appDB.users.insert_one({"_id": myuser.id, \
                                "password": myuser.pw_hash, \
                                "history": []})
            login_user(myuser)
            return redirect(url_for('index'))

@app.route('/static/history.html')
@login_required
def history():
    # Add in more stuff about getting the user's history!
    return render_template('web/history.html', history = current_user.history)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/result', methods=['POST', 'GET'])
def result():
    if(request.method == 'POST'):
        # Do some stuff here with the variables
        source = request.form.get('source')
        destination = request.form.get('destination')


        sourceURL = urllib.parse.quote(source)
        destinationURL = urllib.parse.quote(destination)


        try:
            slat,slong = geo.geocode(source).coordinates
        except:
            return index()

        try:
            dlat,dlong = geo.geocode(destination).coordinates
        except:
            return index()


        dregion = geo.reverse_geocode(dlat,dlong).county

        lots = pms.getLots(dlat, dlong)[:5]


        weather = ws.get_weather(dlat,dlong)

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
            entry['address']= lot['address']+ " "+dregion
            entry['mlat'] = mlat
            entry['mlong'] = mlong
            lotsMarkers.append(entry)

        if current_user.is_authenticated:
            history_item = {
                'time':time.ctime(),
                'source':source,
                'destination':destination,
                'src_latlng':(slat, slong),
                'dst_latlng':(dlat, dlong),
                'uber':ride_estimates_uber,
                'lyft':ride_estimates_lyft,
                'parking':lots,
                'weather':weather
            }
            current_user.add_history_item(history_item)


        return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft, lots=lots, weather=weather, slong=slong,slat=slat,dlong=dlong,dlat=dlat, destinationURL=destinationURL,sourceURL=sourceURL, lotsMarkers=lotsMarkers)

        # return render_template('web/result.html', source=source, destination=destination, uber=ride_estimates_uber, lyft=ride_estimates_lyft, lots=lots)
    else:
        if not current_user.is_authenticated:
            return redirect(url_for("index"))
        mytime = request.args.get("time")
        for item in current_user.history:
            if item['time'] == mytime:
                myitem = item

        sourceURL = urllib.parse.quote(myitem['source'])
        destinationURL = urllib.parse.quote(myitem['destination'])
        lotsMarkers = []
        slat = myitem['src_latlng'][0]
        slong = myitem['src_latlng'][1]
        dlat = myitem['dst_latlng'][0]
        dlong = myitem['dst_latlng'][1]
        dregion = geo.reverse_geocode(dlat,dlong).county
        for lot in myitem['parking']:
            entry={}
            entry['name']= lot['name']
            mlat,mlong = geo.geocode(lot['address']+" "+dregion).coordinates
            entry['mlat'] = mlat
            entry['mlong'] = mlong
            lotsMarkers.append(entry)
        return render_template('web/result.html', source=myitem['source'], \
                                                destination=myitem['destination'], \
                                                uber=myitem['uber'], \
                                                lyft=myitem['lyft'], \
                                                lots=myitem['parking'], \
                                                weather=myitem['weather'], \
                                                slong=slong,\
                                                slat=slat,\
                                                dlong=dlong, \
                                                dlat=dlat, \
                                                destinationURL=destinationURL, \
                                                sourceURL=sourceURL, \
                                                lotsMarkers=lotsMarkers)
