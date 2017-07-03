# Golden-Ticket
[![python version](https://img.shields.io/badge/python-v3.5-green.svg)]()
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

A Twilio-API SMS interface for finding the Golden Hour timings for your location.

## What is the Golden Hour?
As quoted from [Wikipedia](https://goo.gl/8iETFY):
> In photography, the golden hour (sometimes known as magic hour, especially in cinematography) is a period shortly after sunrise or before sunset during which daylight is redder and softer than when the Sun is higher in the sky.

## Set up
1. This repository uses `Python 3`, and uses a *virtualenv* to standardize set-ups. Make sure you have `pip` installed and the repository cloned, and then run the following command in the main directory:
```bash
pip install -r requirements.txt
```

2. Create an account on Twilio.

3. Using the Twilio free trial, verify a potential number that you would want to use (this will be the number that is texting you).

4. Install [ngrok](https://ngrok.com/download) - this will be used to route any webhook calls from Twilio to your local machine.

4. Verify a Phone Number on Twilio (https://www.twilio.com/console/phone-numbers/verified) that you would like to text.

5. Run `ngrok http 5000`, this will create a link that Twilio can use to HTTP POST to (in this case when a message is received).

6. Login to Twilio then navigate to _Twilio Console_ **->** _Phone Numbers_ **->** _Manage Numbers_ **->** _Active Numbers_ **->** _< Your Number >_ , then in the box for _Messaging_ **->** _A message comes in_ paste in the URL shown in ngrok. For instance `https://e31wf4c9.ngrok.io/sms`. Note that `/sms` is appended to the end, since that is how `golden_hour.py` is configured

## Running the application
1. Run the following command in the root directory of the repository
```bash
python3 golden_hour.py
```
2. Send your Twilio number your location, and you'll get sent back the timings for the Golden Hour for your current day

3. Go to a park, high building, mountain during those times and enjoy nature at its finest

## Compatibility issues
Currently the application is configured to parse and return information on a message in a form like this _33°46′45″ N  94°23′24″ W_. On an iPhone this format for your GPS location can be found by copying your location as shown in the native Compass application.

## Logic
Using the following [site](http://www.photopills.com/articles/understanding-golden-hour-blue-hour-and-twilights) to estimate getting the golden hour timings. In the code I use the difference between the end of civil twilight and sunset to estimate how long it takes the sun to go from 6° above the horizon to -4° above the horizon.  
