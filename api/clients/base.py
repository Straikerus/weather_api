import requests

class BaseClient:
    """
    
    Базовый класс для клиента. Включает в себя конструктор и функцию
    для получения погоды в указанном городе.

    """
    errors_dict = {}
    def __init__(self, weather_url, token=None):
        self.weather_url = weather_url
        self.token = token
    
    def get_city_weather(self, city_name):
        """

        Функция для получения погоды в указанном городе.
        Функция делает запрос к источнику, и в случае успешного запроса
        обрабатывает его и возвращает словарь с погодой, либо возвращает
        словарь с ошибкой. Пояснения ошибок по каждому коду ответа
        хранятся в словаре errors_dict у каждого класса клиента.

        """
        try:
            r = requests.get(self.weather_url, self.prepare_request_params(city_name))
            if r.status_code in self.errors_dict.keys():
                result = {
                    'error': self.errors_dict[r.status_code]
                }
            elif r.status_code == 200:
                result = self.handle_response(r)
            else:
                result = {
                    'error': 'Unhandled service response'
                }
        except:
            result = {
                'error': 'Unhandled exception'
            }
        return result
