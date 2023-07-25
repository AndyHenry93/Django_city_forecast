import gspread 
import json
from urllib.request import urlopen
import os
# from dotenv import load_dotenv
# load_dotenv()
import environ
env = environ.Env()
environ.Env.read_env()


# openweather api key saved in an env file 
# api = str(os.getenv("API_KEY"))
api = env("API_KEY")

# List of bad characters in the dataset that must be cleaned
bad_char = [' ','-','/']

# list of avaliable weather condition that the user can call against the openweatherAPI
cond_list = ['Thunderstorm','Drizzle','Rain','Snow','Clear','Clouds','Mist','Smoke','Haze','Dust','Fog','Sand','Dust','Ash','Squall','Tornado']

# google api credentials
credentials = {
  "type": env("type"),
  "project_id": env("project_id"),
  "private_key_id": env("private_key_id"),
  "private_key": env("private_key"),
  "client_email": env("client_email"),
  "client_id": env("client_id"),
  "auth_uri": env("auth_uri"),
  "token_uri": env("token_uri"),
  "auth_provider_x509_cert_url": env("auth_provider_x509_cert_url"),
  "client_x509_cert_url": env("client_x509_cert_url"),
  "universe_domain": env("universe_domain")
}


# def get_data(file,range):
def get_data(range):
    """
    Params: takes two parameters the file and range to be passed for google sheets api connections and validations
    process: passes the file name to the gspread package to begin the api call, next open the sheet with the needed data and save a sh
            pass the sheet property to sh with the range param and save as data.
    return: the dataset 
    """
    # gc = gspread.service_account(filename=file)
    
    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open("interview_US Cities")
    data = sh.sheet1.get(range)
    return data

def clean_dataset(dataset,bad_char_list):
    """
    params: takes two parameters the dataset and list of characters
    process: begins the cleaning process by created an empty list for the cleaned data, runs a for loop through the dataset, entries and characters 
            if the caharacters arew in the entires the character is removed and replaced with openapi friendly syntax 
            next the entires are appened to a new clean list and zipped back together
    return: cleaned dataset 
    """
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
    """
        params: dataset and the api 
        process: passes the starte and city from the cleaned dataset with the api key to the openapi url call
                next the weather data is saved to the city_data variable and unpacked into a dictionary
                the dictionary is then appened to the city data list. 

        return: city weather data 
    """
    city_weather_data = []
    for city, state in dataset:
        source = urlopen('https://api.openweathermap.org/data/2.5/weather?q='+city+','+state+'&appid='+api+'&units=imperial',).read()
        city_data = json.loads(source)
        state = state.replace('+',' ')
        weather_data = {
            "city": str(city_data['name']),
            "state":state,
            "curr_temp":round(float((city_data['main']['temp']))),
            "wind_speed":str(city_data['wind']['speed']),
            "weather_cond":str(city_data['weather'][0]['main'])
            }
        city_weather_data.append(weather_data)          
    return city_weather_data

def user_condition_input(dataset,user_input):
    """
    param: dataset and users form input 
    process: iterates over the city weather data, if the user condition input is in the list 
             add that item to the userdata list
    return: user_dataset
    """
    user_dataset = []
    for item in dataset:
        if user_input == item["weather_cond"]:
            user_dataset.append(item)
    return user_dataset
