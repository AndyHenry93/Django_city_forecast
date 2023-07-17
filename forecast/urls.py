from django.urls import path
from . import views

app_name="forecast"

urlpatterns = [
    # index page url
    path('',views.forecast,name='weather'),
    path('forecast_list/',views.forecast_list,name='forecast_list')

]