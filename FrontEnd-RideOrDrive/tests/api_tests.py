import unittest
from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
from pygeocoder import Geocoder

from lyft_rides.session import Session as LSesh
from lyft_rides.client import LyftRidesClient
from lyft_rides.auth import ClientCredentialGrant

import time

GEOCODE_API = 'AIzaSyAP9d-BJsOwz7XCWhz8FCee-5y133iLot8'

class API_Tests(unittest.TestCase):

    def test_lyft_estimator(self):

        auth_flow = ClientCredentialGrant(
            'd-0DVSBkAukU',
            'I-yZZtV1WkY_903WKVqZEfMEls37VTCa',
            'rides.request',
            )
        session = auth_flow.get_session()

        client = LyftRidesClient(session)
        response = client.get_cost_estimates(37.7833, -122.4167, 37.791,-122.405)
        self.assertTrue(response != None)

    def test_uber_estimator(self):
        session = Session(server_token='hVj-yE_w4iJQ5-rbp8hmKZSNekOzLV1cvnF_BrNl')
        client = UberRidesClient(session)
        response = client.get_price_estimates(
            start_latitude=37.770,
            start_longitude=-122.411,
            end_latitude=37.791,
            end_longitude=-122.405,
            seat_count=2
        )
        self.assertTrue(response != None)


    def test_google_maps_request(self):
        geo = Geocoder(api_key=GEOCODE_API)

        self.assertEqual(geo.geocode("Dallas, Texas").coordinates, (32.7766642, -96.79698789999999))
        self.assertEqual(geo.geocode("Austin, Texas").coordinates, (30.267153, -97.7430608))
        self.assertEqual(geo.geocode("University of Texas at Austin").coordinates, (30.2849185, -97.7340567))
        self.assertEqual(geo.geocode("UT Austin").coordinates, (30.2849185, -97.7340567))

    def test_time_google_api(self):
        geo = Geocoder(api_key=GEOCODE_API)

        start=time.time()
        geo.geocode("University of Texas at Austin")
        end = time.time()
        self.assertTrue(1 > end-start, "Single geocoder is Slower than 1s")

    def test_time_uber_api(self):
        session = Session(server_token='hVj-yE_w4iJQ5-rbp8hmKZSNekOzLV1cvnF_BrNl')
        client = UberRidesClient(session)

        start = time.time()
        response = client.get_price_estimates(
            start_latitude=37.770,
            start_longitude=-122.411,
            end_latitude=37.791,
            end_longitude=-122.405,
            seat_count=2
        )
        end = time.time()

        self.assertTrue(2 > end-start, "Uber API Request takes longer than 2s")

    def test_time_lyft_api(self):
        auth_flow = ClientCredentialGrant(
            'd-0DVSBkAukU',
            'I-yZZtV1WkY_903WKVqZEfMEls37VTCa',
            'rides.request',
            )
        session = auth_flow.get_session()

        client = LyftRidesClient(session)
        start = time.time()
        response = client.get_cost_estimates(37.7833, -122.4167, 37.791,-122.405)
        end = time.time()
        self.assertTrue(1 > end-start)

    def test_google_uber_pipe(self):
        geo = Geocoder(api_key=GEOCODE_API)

        dlat,dlong = geo.geocode("UT Austin").coordinates
        alat,along = geo.geocode("Round Rock, TX").coordinates

        session = Session(server_token='hVj-yE_w4iJQ5-rbp8hmKZSNekOzLV1cvnF_BrNl')
        client = UberRidesClient(session)

        start = time.time()
        response = client.get_price_estimates(
            start_latitude=dlat,
            start_longitude=dlong,
            end_latitude=alat,
            end_longitude=along,
            seat_count=2
        )
        end = time.time()
        self.assertTrue(response != None)
#        print(response.json.get('prices'))

    def test_google_lyft_pipe(self):
        geo = Geocoder(api_key=GEOCODE_API)

        auth_flow = ClientCredentialGrant(
            'd-0DVSBkAukU',
            'I-yZZtV1WkY_903WKVqZEfMEls37VTCa',
            'rides.request',
            )
        session = auth_flow.get_session()

        client = LyftRidesClient(session)
        start = time.time()


        dlat,dlong = geo.geocode("UT Austin").coordinates
        alat,along = geo.geocode("Round Rock, TX").coordinates
        response = client.get_cost_estimates(dlat,dlong,alat,along)

        end = time.time()
        self.assertTrue(5 > end-start)
    #        print(response.json.get('prices'))

    def test_google_lyft_uber_pipe(self):
        geo = Geocoder(api_key=GEOCODE_API)

        sessionu = Session(server_token='hVj-yE_w4iJQ5-rbp8hmKZSNekOzLV1cvnF_BrNl')
        clientu = UberRidesClient(sessionu)

        auth_flow = ClientCredentialGrant(
            'd-0DVSBkAukU',
            'I-yZZtV1WkY_903WKVqZEfMEls37VTCa',
            'rides.request',
            )
        session = auth_flow.get_session()

        client = LyftRidesClient(session)
        start = time.time()

        dlat,dlong = geo.geocode("UT Austin").coordinates
        alat,along = geo.geocode("Round Rock, TX").coordinates
        response = client.get_cost_estimates(dlat,dlong,alat,along)
        response = clientu.get_price_estimates(
            start_latitude=dlat,
            start_longitude=dlong,
            end_latitude=alat,
            end_longitude=along,
            seat_count=2
        )

        end = time.time()
        self.assertTrue(10 > end-start)
    #        print(response.json.get('prices'))

if __name__ == '__main__':
    unittest.main()
