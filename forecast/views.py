from django.shortcuts import render
import os
from . forms import ForecastForm
from . utils import get_data, clean_dataset, weather_api
from django.contrib import messages


# getting the openweather api key and assigning to the variable api
api = str(os.getenv('API_KEY'))
 # List of characer in the dataset to be removed during data cleaning process
bad_char = [' ','-','/']
def forecast(request):
    data = get_data(file='creds.json',range='A2:B')
   
    cleaned_dataset = clean_dataset(dataset=data, bad_char_list=bad_char)

    city_data = weather_api(dataset=cleaned_dataset,api=api)

    if request.method == "POST":
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
    




#  city_weather_data = []
    # for city, state in dataset:
    #     source = urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+','+state+'&appid='+api+'&units=imperial').read()
    #     city_data = json.loads(source)
    #     state = state.replace('+',' ')
    #     # TODO: Add logic to not add duplicates, try to set timer, if changes in windspeed, curr_temp, or weathercond change the data
    #     weather_data = Weather(city=str(city_data['name']),
    #                            state=state,
    #                            curr_temp=round(float((city_data['main']['temp']))),
    #                            wind_speed=str(city_data['wind']['speed']),
    #                            weather_cond=str(city_data['weather'][0]['main']))
    #     if weather_data
    #     city_weather_data.append(weather_data)   
# for item in city_weather_data:
# weather_data_set=db.objects.bulk_create(city_weather_data)




# weather_data = Weather(city=weather_data["city"],
 #                        state=state,
 #                        curr_temp=weather_data["curr_temp"],
#                        wind_speed = weather_data["windspeed"],
#                        weather_cond = weather_data["weather_cond"])
 # city_weather_data.append(weather_data)
# weather_data_set=Weather.objects.bulk_create(city_weather_data)



# def forecast(request):
#     """
    
#     """
#     data = get_data(file='creds.json',range='A2:B')
   
#     cleaned_dataset = clean_dataset(dataset=data, bad_char_list=bad_char)

#     populate_db(dataset=cleaned_dataset,api=api)

#     if request.method == "POST":
#         form = ForecastForm(request.POST)
#         if form.is_valid():
#             weather_condition = form.cleaned_data['weather_cond'].lower().title()
#             city_data = Weather.objects.filter(weather_cond=weather_condition)
#             context ={
#                 "city_data":city_data,
#                 "weather_cond": weather_condition
#             }
#             # messages.success("Some successful message")
#             return render(request,'forecast/forecast.html',context )  
#         # else:
#         #     messages.error("Some error message")    
#     else:
#         form = ForecastForm()
#         return render(request,'forecast/forecast.html',{'form':form})