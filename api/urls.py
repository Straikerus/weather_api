from django.urls import path
from api import views

urlpatterns = [
    path('update-cities', views.UpdateCitiesWeatherView.as_view()),
    path('get-weather', views.CityWeatherView.as_view()),
]
