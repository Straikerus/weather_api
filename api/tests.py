import json
from django.test import TestCase, RequestFactory
from django.conf import settings
from . import views

class ClientsTests(TestCase):
    # Тест каждого клиента
    def test_clients_availability(self):
        for client_object in settings.SOURCES_DICT.values():
            self.assertEqual('error' in client_object.get_city_weather('tomsk'), False)


class UpdateCitiesWeatherViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_request_without_cities_list_handle(self):
        request = self.factory.post('/api/update-cities')
        response = views.UpdateCitiesWeatherView.as_view()(request)
        description = json.loads(response._container[0].decode('utf-8'))['description']
        self.assertEqual(response.status_code, 500)
        self.assertEqual(description, 'cities_list value has not been sent')

    def test_empty_cities_list_handle(self):
        request = self.factory.post('/api/update-cities')
        request.POST = {
            'cities_list': '[]'
        }
        response = views.UpdateCitiesWeatherView.as_view()(request)
        description = json.loads(response._container[0].decode('utf-8'))['description']
        self.assertEqual(response.status_code, 500)
        self.assertEqual(description, 'Cities list is empty')
    
    def test_wrong_cities_list_format_handle(self):
        request = self.factory.post('/api/update-cities')
        request.POST = {
            'cities_list': 'test'
        }
        response = views.UpdateCitiesWeatherView.as_view()(request)
        description = json.loads(response._container[0].decode('utf-8'))['description']
        self.assertEqual(response.status_code, 500)
        self.assertEqual(description, 'Wrong cities list format. It should be array with cities names')


class CityWeatherViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_request_without_city_handle(self):
        request = self.factory.get('/api/get-weather')
        response = views.CityWeatherView.as_view()(request)
        description = json.loads(response._container[0].decode('utf-8'))['description']
        self.assertEqual(response.status_code, 500)
        self.assertEqual(description, 'city value has not been sent')

    def test_no_weather_for_city_handle(self):
        request = self.factory.get('/api/get-weather')
        request.GET = {
            'city': 'tomsk'
        }
        response = views.CityWeatherView.as_view()(request)
        description = json.loads(response._container[0].decode('utf-8'))['description']
        self.assertEqual(response.status_code, 404)
        self.assertEqual(description, 'Cannot find weather for this city')
    
    def test_wrong_city_name_format_handle(self):
        request = self.factory.get('/api/get-weather')
        request.GET = {
            'city': 123
        }
        response = views.CityWeatherView.as_view()(request)
        description = json.loads(response._container[0].decode('utf-8'))['description']
        self.assertEqual(response.status_code, 500)
        self.assertEqual(description, 'Wrong city name format, it must be a string value')
