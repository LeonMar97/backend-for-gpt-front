from flask import Flask, redirect, render_template, request, jsonify
from flask_cors import CORS
import json
import requests
from datetime import datetime
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz
app = Flask(__name__)
CORS(app)


@app.route("/")
def main():
    return render_template("index.html")

def time_by_zone(lat:str,long:str)->datetime:
    '''function gets lat and long, returns
    current time as datetime object'''
    
    timez_str=TimezoneFinder().timezone_at(lat=lat,lng=long)
    return datetime.now(pytz.timezone(timez_str))

@app.route("/weather")
def weater_by_city():
    # SHOULD MAKE AN EXCEPTION FOR COUNTRY NOT FOUND
    country,city=request.args["country"],request.args["city"]
    lat, long = find_lat_long(city, country).values()
    print("lat: ", lat, "long:", long)
    weather_json = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": long,
            "hourly": "temperature_2m",
            "cell_selection": "nearest",
        },
    ).json()

    current_time = time_by_zone(lat=lat,long=long)
    
    ret_json = {
        "name": [request.args["city"], request.args["country"]],
        "time": current_time.strftime("%H:%M:%S"),
        "temp": weather_json["hourly"]["temperature_2m"][current_time.hour],
    }

    return jsonify(ret_json)


def find_lat_long(city: str, country: str) -> dict:
    resp = requests.get(
        f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    ).json()
    for cur_country in resp["results"]:
        if cur_country["country"] == country.title():
            lat, long = cur_country["latitude"], cur_country["longitude"]
            return {"lat": lat, "long": long}

    #!!!SHOULD CREATE AN EXCEPTION RETURN FOR THAT CASE!!!!
    return {"lat": "ERROR", "long": "ERROR"}


if __name__ == "__main__":
    app.run(port=8080)
