from django.db import models

class Weather(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    curr_temp = models.CharField(max_length=100)
    wind_speed = models.CharField(max_length=100)
    weather_cond = models.CharField(max_length=100)

    def __str__(self):
        return self.city
    
    class Meta:
        verbose_name_plural = 'cities'