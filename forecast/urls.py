from django.urls import path
from . import views

app_name="forecast"

urlpatterns = [
    # index page url
    path('',views.forecast,name='weather' ),
]