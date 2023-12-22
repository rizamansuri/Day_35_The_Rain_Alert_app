# OpenWeatherMap current weather API documentation https://openweathermap.org/current
# Get current latitude and longitude from https://www.latlong.net/
# Link to your OpenWeatherMap API key req, login https://home.openweathermap.org/api_keys
# Online JSON viewer https://jsonviewer.stack.hu/
# Find a place that is raining https://www.ventusky.com/
# To run python in cloud and schedule its execution https://www.pythonanywhere.com/

import os
import requests
from twilio.rest import Client

OWM_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
api_key = os.environ.get("OWM_API_KEY")

parameters = {
    "lat": 52.520008,
    "lon": 13.404954,
    "appid": api_key,
    "cnt": 4
}

response = requests.get(OWM_endpoint, params=parameters)
response.raise_for_status()  # raises exception if cannot connect to endpoint

weather_data = response.json()
# print(weather_data["list"][0]["weather"][0]['id'])
will_rain = False
for hour_data in weather_data["list"]:
    condition_data = hour_data["weather"][0]['id']
    if int(condition_data) < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
    .create(
        body="It's going to rain today, remember to bring an umbrella ☔"
             "\nMessage sent by Riza's Python Project (22-12-2023, Friday)",
        from_=os.environ.get("SEND_FROM_MOBILE_NUMBER"),
        to=os.environ.get("SEND_TO_MOBILE_NUMBER")
    )
print(message.status)
