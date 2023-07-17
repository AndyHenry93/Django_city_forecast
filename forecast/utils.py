import gspread 
import json
from urllib.request import urlopen

def get_data(file,range):
    # Using gspread to call the google sheets api and saving the dataset to the data variable
    gc = gspread.service_account(filename=file)
    sh = gc.open("interview_US Cities")
    data = sh.sheet1.get(range)
    return data

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
