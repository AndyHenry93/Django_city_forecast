from django.shortcuts import render
import os
from . forms import ForecastForm
from . utils import get_data, clean_dataset, weather_api
from django.contrib import messages

# from . tasks import weather_api

# getting the openweather api key and assigning to the variable api
api = str(os.getenv('API_KEY'))
 # List of characer in the dataset to be removed during data cleaning process
bad_char = [' ','-','/']
data = get_data(file='creds.json',range='A2:B')
cleaned_dataset = clean_dataset(dataset=data, bad_char_list=bad_char)

def forecast(request):
    if request.method == "POST":
        # future update to implement Celery and redis
        # city_data = weather_api.delay(cleaned_dataset,api)
        # city_data = city_data.get()
        
        city_data = weather_api(dataset=cleaned_dataset,api=api)
        form = ForecastForm(request.POST)
        if form.is_valid():
            weather_condition = form.cleaned_data['weather_cond'].lower().title()
            context ={
                "city_data":city_data,
                "weather_cond": weather_condition,
            }
            # messages.success("Some successful message")
            return render(request,'forecast/forcast_results.html',context )  
        # else:
        #     messages.error("Some error message")    
    else:
        form = ForecastForm()
        return render(request,'forecast/forecast.html',{'form':form})