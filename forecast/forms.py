from django import forms

# weather condition list from the utils directory to process form validation
from . utils import cond_list

# form that takes the user input for a weather condition
class ForecastForm(forms.Form):
    weather_cond = forms.CharField(label="Type a weather condition", max_length=100, required=True)
    
    def clean_weather_cond(self):
        """
            Function that preforms an addition form validator:
            the function checks weather the user entered a weather condition from the list of provided conditions
            if the user input isnt in the list a form validation error is raised
            else the data is returned
        """
        data = self.cleaned_data.get("weather_cond").lower().title()
        if data not in cond_list:
            raise forms.ValidationError("Please only use weather conditions provided below")
        return data
