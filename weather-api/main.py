from flask import Flask,redirect,render_template,request,jsonify
import json
import requests
app=Flask(__name__)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/weather")
def weater_by_city():
    #SHOULD MAKE AN EXCEPTION FOR COUNTRY NOT FOUND
    lat,long=find_lat_long(request.args['city'],request.args['country']).values()
    weather_json=requests.get(f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m').json()
    return jsonify(weather_json)

def find_lat_long(city:str,country:str)->dict:
    resp=requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={city}").json()
    for cur_country in resp['results']:
        if cur_country['country']==country.title():
            lat,long=cur_country['latitude'],cur_country['longitude']
            return ({'lat':lat,'long':long})
    #!!!SHOULD CREATE AN EXCEPTION RETURN FOR THAT CASE!!!!
    return({'lat':"ERROR",'long':"ERROR"})

    


if __name__=="__main__":
    app.run(port=8080)