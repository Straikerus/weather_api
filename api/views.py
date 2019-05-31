import ast
from api.utils import update_cities, get_city_weather
from django.http import JsonResponse, HttpResponse
from django.views.generic import View


class UpdateCitiesWeatherView(View):
    # Для запроса на обновление погоды городов выбран именно метод post,
    # так как происходит взаимодействие с БД и изменение данных на сервере,
    # поэтому решил, что будет правильнее использовать именно метод post
    def post(self, request, *args, **kwargs):
        cities_list = request.POST.get('cities_list')
        if not cities_list:
            data = {
                'description': 'cities_list value has not been sent'
            }
            return JsonResponse(data, status=500)
        try:
            if not isinstance(cities_list, list):
                cities_list = ast.literal_eval(cities_list)
                if not isinstance(cities_list, list):
                    data = {
                        'description': 'Wrong cities list format. It should be array with cities names'
                    }
                    return JsonResponse(data, status=500)
            if len(cities_list) == 0:
                data = {
                        'description': 'Cities list is empty'
                }
                return JsonResponse(data, status=500)
        except:
            data = {
                'description': 'Wrong cities list format. It should be array with cities names'
            }
            return JsonResponse(data, status=500) 
        if len(cities_list) == 0:
            data = {
                'description': 'Empty cities list'
            }
            return JsonResponse(data, status=500)
        error_logs = update_cities(cities_list)
        if len(error_logs) > 0:
            data = {
                'errors': error_logs
            }
            return JsonResponse(data, status=500)
        return HttpResponse()


class CityWeatherView(View):
    def get(self, request, *args, **kwargs):
        city = request.GET.get('city')
        if not city:
            data = {
                'description': 'city value has not been sent'
            }
            return JsonResponse(data, status=500)
        if not isinstance(city, str):
            data = {
                'description': 'Wrong city name format, it must be a string value'
            }
            return JsonResponse(data, status=500)
        weather = get_city_weather(city)
        if len(weather) == 0:
            data = {
                'description': 'Cannot find weather for this city'
            }
            return JsonResponse(data, status=404)
        data = {
            'weather': weather
        }
        return JsonResponse(data)
        
