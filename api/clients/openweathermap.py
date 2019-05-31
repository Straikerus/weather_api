from api.clients import BaseClient


class OpenWeatherMap(BaseClient):
    errors_dict = {
        404: 'Cannot find weather for this city',
        429: 'API limit of calls exceeded',
    }

    def handle_response(self, response):
        data = response.json()

        # Возвращается именно словарь, а не просто температура,
        # для будущего расширения, например добавятся новые поля
        result = {
            'temperature': float(data['main']['temp'])
        }
        return result
    
    def prepare_request_params(self, city_name):
        params = {'q': city_name, 'appid': self.token, 'units': 'metric'}
        return params
