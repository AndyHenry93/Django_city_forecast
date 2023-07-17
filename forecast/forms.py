from django import forms
from . utils import cond_list


class ForecastForm(forms.Form):
    weather_cond = forms.CharField(label="Type a weather condition", max_length=100, required=True)
    
    def clean_weather_cond(self):
        data = self.cleaned_data.get("weather_cond").lower().title()
        if data not in cond_list:
            raise forms.ValidationError("Please only use weather conditions provided below")
        return data
