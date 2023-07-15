from django import forms

class ForecastForm(forms.Form):
    weather_cond = forms.CharField(label="Type a weather condition", max_length=100, required=True)