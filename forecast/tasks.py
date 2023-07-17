# Task file that will automate calling the openweatherAPI to speed HTTPRESPONDS timing

from __future__ import absolute_import, unicode_literals
from celery import shared_task
import json
from urllib.request import urlopen
from django.contrib import messages

@shared_task
def weather_api(dataset,api):
    city_weather_data = []
    for city, state in dataset:
        source = urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+','+state+'&appid='+api+'&units=imperial',).read()
        city_data = json.loads(source)
        state = state.replace('+',' ')
        # TODO: Add logic to not add duplicates, try to set timer, if changes in windspeed, curr_temp, or weathercond change the data
        weather_data = {
            "city": str(city_data['name']),
            "state":state,
            "curr_temp":round(float((city_data['main']['temp']))),
            "wind_speed":str(city_data['wind']['speed']),
            "weather_cond":str(city_data['weather'][0]['main'])
            }
        if weather_data["city"] not in city_weather_data:
            city_weather_data.append(weather_data)          
    return city_weather_data

# @shared_task
# def processing_api():
#     return messages.info(request, "Processing, will return information soon")



