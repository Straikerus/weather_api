import requests
from api.clients import BaseClient
from bs4 import BeautifulSoup


class YandexWeather(BaseClient):
    errors_dict = {
        404: 'Cannot find weather for this city',
    }

    def handle_response(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        temperature_value = soup.findAll(
            'div', {'class':'fact__temp'}
        )[0].find('span', {'class': 'temp__value'}).text

        # Возвращается именно словарь, а не просто температура,
        # для будущего расширения, например добавятся новые поля
        result = {
            'temperature': float(temperature_value)
        }
        return result

    def get_city_weather(self, city_name):
        try:
            r = requests.get(self.weather_url + city_name)
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
