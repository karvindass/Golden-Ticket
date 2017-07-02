import os
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/sms", methods=['GET','POST'])
def sms_reply():
    resp = MessagingResponse()

    incoming_message_body = request.values.get('Body')
    print ("Full incoming message body:", incoming_message_body)

    # Parsing for coordinates similar to
    # 33°46′45″ N  94°23′24″ W

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
    print("New calculated values", latitude_decimal, longitude_decimal)

    # TODO make http request
    # TODO do estimate for golden hour
    # TODO form string to return
    # TODO respond with message

    resp.message("Message receipt confirmed")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
