from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import InputForm
from RideOrDrive.settings import secrets
import os
import geocoder

os.environ["GOOGLE_API_KEY"] = secrets['google_api_key ']

# Create your views here.

def calc(request):
    if request.method == "POST":
        my_input = InputForm(request.POST)
        if my_input.is_valid():
            my_input.save()

            # Now do some calculations
            # Use Geocoding API to get location string of start and end
            calc_data = my_input.cleaned_data
            calc_data['source'] = geocoder.google([calc_data['start_lat'], calc_data['start_long']], method='reverse')
            calc_data['dest'] = geocoder.google([calc_data['end_lat'], calc_data['end_long']], method='reverse')

            # then use Uber + Lyft APIs to get the prices

            return JsonResponse(calc_data)
        else:
            return HttpResponse(status=400)


