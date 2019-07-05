from django.urls import path

from .views import WeatherInfoView

urlpatterns = [
    path('', WeatherInfoView.as_view(), name='weather-info')
]
