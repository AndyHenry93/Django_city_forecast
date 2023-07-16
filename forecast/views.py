from django.shortcuts import render
import os
import gspread 
import json
from urllib.request import urlopen
from django.contrib import messages
from . forms import ForecastForm
from . models import Weather

# getting the openweather api key and assigning to the variable api
api = str(os.getenv('API_KEY'))
 # List of characer in the dataset to be removed during data cleaning process
bad_char = [' ','-','/']

# google sheets api helper function
def get_data(file,range):
    # Using gspread to call the google sheets api and saving the dataset to the data variable
    gc = gspread.service_account(filename=file)
    sh = gc.open("interview_US Cities")
    data = sh.sheet1.get(range)
    return data

# Data cleaning helper function
def clean_dataset(dataset,bad_char_list):
    bad_char = bad_char_list
    cities = dataset
    cleaned_data = []

    for item in cities:
        for value in item:
            for char in bad_char:
                if char in value:
                    if char == ' ':
                        value = value.replace(' ','+')
                    if char == '-':
                        value = value.split('-',1)[0]
                    if char == '/':
                        value = value.split('/',1)[0]
            if char not in value:
                cleaned_data.append(value)
    cleaned_data = list(zip(cleaned_data[::2],cleaned_data[1::2]))
    return cleaned_data

# openweather api helper function
def populate_db(dataset,api):
    city_weather_data = []
    for city, state in dataset:
        source = urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+','+state+'&appid='+api+'&units=imperial').read()
        city_data = json.loads(source)
        state = state.replace('+',' ')
        # TODO: Add logic to not add duplicates, try to set timer, if changes in windspeed, curr_temp, or weathercond change the data
        weather_data = Weather(city=str(city_data['name']),
                               state=state,
                               curr_temp=round(float((city_data['main']['temp']))),
                               wind_speed=str(city_data['wind']['speed']),
                               weather_cond=str(city_data['weather'][0]['main']))
        city_weather_data.append(weather_data)
    weather_data_set=Weather.objects.bulk_create(city_weather_data,ignore_conflicts=True)

def forecast(request):
    """
    
    """
    data = get_data(file='creds.json',range='A2:B')
   
    cleaned_dataset = clean_dataset(dataset=data, bad_char_list=bad_char)

    populate_db(dataset=cleaned_dataset,api=api)

    if request.method == "POST":
        form = ForecastForm(request.POST)
        if form.is_valid():
            weather_condition = form.cleaned_data['weather_cond'].lower().title()
            city_data = Weather.objects.filter(weather_cond=weather_condition)
            context ={
                "city_data":city_data,
                "weather_cond": weather_condition
            }
            # messages.success("Some successful message")
            return render(request,'forecast/forecast.html',context )  
        # else:
        #     messages.error("Some error message")    
    else:
        form = ForecastForm()
        return render(request,'forecast/forecast.html',{'form':form})