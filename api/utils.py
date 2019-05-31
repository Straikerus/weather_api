import datetime
from django.conf import settings
from .models import Weather

def update_cities(cities_list):
    """

    Получение акутальных данных о погоде со всех источников.
    Входными данными является список с названями городов.
    Выходными данными является словарь с ошибками,
    либо пустой словарь, если ошибок не было.
    Пример выходных данных:
    {
        "tomsk": {
            "yandex": "Cannot find weather for this city",
            "openweathermap": "API limit of calls exceeded"
        }
    }

    """
    error_logs = {}
    for city in cities_list:
        if not isinstance(city, str):
            city = str(city)
            error_logs[city] = 'Wrong city format'
            continue
        city_errors = {}
        for source_name, source_client_object in settings.SOURCES_DICT.items():
            result = source_client_object.get_city_weather(city)
            if 'error' in result:
                city_errors[source_name] = result['error']
                continue
            Weather.objects.create(
                city=city.lower(),
                temperature=result['temperature'],
                source=source_name,
                date=datetime.datetime.now()
            )
        if len(city_errors) > 0:
            error_logs[city] = city_errors
    return error_logs

def get_city_weather(city):
    """

    Получение акутальных данных о погоде в городе из базы данных.
    Входными данными является название города.
    Выходными данными является словарь с последней полученной из каждого источника
    информацией о погоде, либо пустой словарь, если нет данных ни из одного источника.
    В случае, если данные о погоде в городе есть только из некоторых источников,
    то для источников, из которых данных нет, в словарь будет записываться пояснение.
    Пример выходных данных:
    {
        "yandex": {"temperature": 16.0, "timestamp": 1559324186.442324},
        "openweathermap": "Cannot find weather from this source"
    }

    """
    result = {}
    at_least_one = False
    for source_name in settings.SOURCES_DICT.keys():
        try:
            weather = Weather.objects.filter(
                city=city.lower(),
                source=source_name
            ).latest(
                'date'
            )
            result[source_name] = {
                'temperature': weather.temperature,
                'timestamp': weather.date.timestamp()
            }
            at_least_one = True
        except Weather.DoesNotExist:
            result[source_name] = 'Cannot find weather from this source'
    if not at_least_one:
        result = {}
    return result
