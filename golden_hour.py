import os
import requests
import json
import time
from datetime import datetime

from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])
def sms_reply():
    resp = MessagingResponse()

    incoming_message_body = request.values.get('Body')
    print ("Full incoming message body:", incoming_message_body)

    # Parsing for coordinates similar to 33°46′45″ N  94°23′24″ W

    latitude_full = incoming_message_body.split(" ")[0]
    if (incoming_message_body.split(" ")[1] == "N"):
        latitude_normalizer = float(1)
    else:
        latitude_normalizer = float(-1)
    longitude_full = incoming_message_body.split(" ")[3]
    if (incoming_message_body.split(" ")[4] == "E"):
        longitude_normalizer = float(1)
    else:
        longitude_normalizer = float(-1)
    print("Parsed values:", latitude_full, longitude_full)

    latitude_full = latitude_full.replace("°"," ")
    latitude_full = latitude_full.replace("′"," ")
    latitude_full = latitude_full.replace("″"," ")

    longitude_full = longitude_full.replace("°"," ")
    longitude_full = longitude_full.replace("′"," ")
    longitude_full = longitude_full.replace("″"," ")
    print("New parsed values:", latitude_full, longitude_full)

    latitude_degree = float(latitude_full.split(" ")[0])
    latitude_minute = float(latitude_full.split(" ")[1])
    latitude_second = float(latitude_full.split(" ")[2])
    longitude_degree = float(longitude_full.split(" ")[0])
    longitude_minute = float(longitude_full.split(" ")[1])
    longitude_second = float(longitude_full.split(" ")[2])

    latitude_decimal = latitude_normalizer * float(latitude_degree + (latitude_minute / 60) + (latitude_second / 3600))
    longitude_decimal = longitude_normalizer * float(longitude_degree + (longitude_minute / 60) + (longitude_second / 3600))
    print("Calculated coordinates", latitude_decimal, longitude_decimal)

    sun_api_response = requests.get('https://api.sunrise-sunset.org/json', params={'lat':latitude_decimal,'lng':longitude_decimal,'date':'today'})
    print(sun_api_response.json()["status"])

    # {"status": "OK", "results": {
    # "day_length": "14:20:48",
    # "sunset": "12:52:12 AM",
    # "civil_twilight_end": "1:21:03 AM",
    # "nautical_twilight_end": "1:56:34 AM",
    # "astronomical_twilight_end": "2:35:19 AM"}}
    # "astronomical_twilight_begin": "8:48:17 AM",
    # "nautical_twilight_begin": "9:27:02 AM",
    # "civil_twilight_begin": "10:02:33 AM",
    # "sunrise": "10:31:24 AM",
    # "solar_noon": "5:41:48 PM",

    sun_data = sun_api_response.json()
    time_format = '%H:%M:%S %p'
    sunrise_time = datetime.strptime(sun_data['results']['sunrise'], time_format)
    sunset_time = datetime.strptime(sun_data['results']['sunset'], time_format)
    civil_twilight_end_time = datetime.strptime(sun_data['results']['civil_twilight_end'], time_format)

    # FIXME Incorrectly parsing time values (AM/PM not going correctly for sunrise time)
    # TODO convert from UTC to local
    # sunset_time = sunset_time.replace(tzinfo='UTC')
    # civil_twilight_end_time = civil_twilight_end_time.replace(tzinfo='UTC')
    # sunset_time = sunset_time.astimezone('America/New_York')
    # civil_twilight_end_time = civil_twilight_end_time.astimezone('America/New_York')

    tdelta = civil_twilight_end_time - sunset_time
    print(type(tdelta))
    print(type(sunset_time))
    # print(tdelta.strftime(time_format))
    print(sun_data['results']['sunset'],sunset_time.strftime(time_format))
    print(sun_data['results']['civil_twilight_end'],civil_twilight_end_time.strftime(time_format))

    golden_hour_start_time = sunset_time - tdelta
    golden_hour_end_time = sunset_time + (4.0 / 6.0) * tdelta

    print(type(golden_hour_start_time))
    print(golden_hour_start_time.strftime(time_format))
    print(type(golden_hour_end_time))
    print(golden_hour_end_time.strftime(time_format))

    # TODO Use Google Maps API timezone to determine time
    # Use time difference between civil twilight and sunset to determine golden hour offset

    resp.message("Golder Hour is from " + golden_hour_start_time.strftime(time_format) + " UTC to " + golden_hour_end_time.strftime(time_format) + " UTC with sunset at " + sunset_time.strftime(time_format) + " UTC")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
