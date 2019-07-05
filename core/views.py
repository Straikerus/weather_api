from django.views.generic import View
from django.shortcuts import render

from api.models import City
from .utils import format_weather


class WeatherInfoView(View):
    def get(self, request, *args, **kwargs):
        weather_rows = City.objects.raw(
            "SELECT * FROM api_city INNER JOIN\
             api_weather ON api_city.id = api_weather.city_id\
             INNER JOIN(SELECT MAX(date) AS latest_date, city_id, source\
             FROM api_weather WHERE date<='2019-07-04 15:50'\
             GROUP BY city_id, source) t2\
             ON api_weather.city_id = t2.city_id\
             AND api_weather.source = t2.source\
             AND api_weather.date = t2.latest_date"
        )
        city_weather = format_weather(weather_rows)
        return render(request, 'core/test.html', {'city_weather': dict(city_weather)})


"""

Запрос для получения актуальной погоды по каждому городу от каждого источника

SELECT * FROM api_city INNER JOIN api_weather ON api_city.id = api_weather.city_id INNER JOIN
(
    SELECT MAX(date) AS latest_date, city_id, source FROM api_weather WHERE date<='2019-07-04 15:50' GROUP BY city_id, source
) t2
ON api_weather.city_id = t2.city_id AND api_weather.source = t2.source AND api_weather.date = t2.latest_date

"""


"""

ORM вариант
Вложенный запрос Weather.objects.filter(date__lte=datetime.datetime.now()).values('city_id', 'source').annotate(latest_date=Max('date'))

"""
