from django.urls import path

from .views import WeatherInfoView, WeatherInfoSlowView

urlpatterns = [
    path('', WeatherInfoView.as_view(), name='weather-info'),
    path('slow', WeatherInfoSlowView.as_view(), name='slow-weather-info')
]
