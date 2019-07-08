import datetime
from django.views.generic import View
from django.shortcuts import render
from collections import defaultdict

from api.models import City, Weather
from .utils import format_weather_rows


class WeatherInfoView(View):
    def get(self, request, *args, **kwargs):
        now_datetime = datetime.datetime.now()
        weather_rows = Weather.objects.raw(
            "SELECT * FROM api_city INNER JOIN\
             api_weather ON api_city.id = api_weather.city_id\
             INNER JOIN(SELECT MAX(datetime) AS latest_date, city_id, source\
             FROM api_weather WHERE datetime<='{now_datetime}'\
             GROUP BY city_id, source) t2\
             ON api_weather.city_id = t2.city_id\
             AND api_weather.source = t2.source\
             AND api_weather.datetime = t2.latest_date".format(
                now_datetime=now_datetime
            )
        )
        city_weather_dict = format_weather_rows(weather_rows)
        return render(
            request,
            'core/test.html',
            {'city_weather_dict': dict(city_weather_dict)}
        )


class WeatherInfoSlowView(View):
    def get(self, request, *args, **kwargs):
        city_weather_dict = defaultdict(list)
        cities_list = City.objects.all()
        sources_list = Weather.objects.values_list('source', flat=True) \
                                      .distinct()
        now_datetime = datetime.datetime.now()
        for city in cities_list:
            for source in sources_list:
                actual_weather = Weather.objects.filter(
                    city=city,
                    source=source,
                    datetime__lte=now_datetime
                ).order_by('-datetime').first()
                city_weather_dict[city.name].append(actual_weather)
        return render(
            request,
            'core/test.html',
            {'city_weather_dict': dict(city_weather_dict)}
        )


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
