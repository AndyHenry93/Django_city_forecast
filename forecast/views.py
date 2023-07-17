from django.shortcuts import render, redirect
from . forms import ForecastForm
from . utils import get_data, clean_dataset, weather_api, user_condition_input,bad_char, api
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from . tasks import weather_api

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
            user_cond = user_condition_input(city_data,weather_condition)

            request.session['user_cond'] = user_cond
            request.session['weather_condition'] = weather_condition
            return redirect("forecast:forecast_list")
        else:
            messages.warning(request, "Please use weather condition in list provide below")
            return redirect("forecast:weather")
    else:
        form = ForecastForm()
        return render(request,'forecast/forecast.html',{'form':form})

def forecast_list(request):
        user_cond = request.session["user_cond"]
        weather_condtion = request.session["weather_condition"]

        # setup pagination 
        paginator = Paginator(user_cond, 6) 
        page = request.GET.get('page')
        try:
            cities = paginator.page(page)
        except PageNotAnInteger:
            cities = paginator.page(1)
        except EmptyPage:
            cities = paginator.page(paginator.num_pages)

        context ={
                "weather_cond": weather_condtion,
                "cities":cities,
            }
        return render(request,'forecast/forecast_results.html',context )
