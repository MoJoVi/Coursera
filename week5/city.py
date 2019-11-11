"""
Задача:
Написать программу для определения погоды в заданном городе.
"""
import requests
from _city_secrets import host, key, my_city


class CityInfo:
    """
    Экземпляры данного класса делают запрос на врешний API (используется
    ресурс "rapidapi.com") и возвращают необходимые значения в словаре
    """
    url = "https://community-open-weather-map.p.rapidapi.com/weather"

    headers = {
        'x-rapidapi-host': host,
        'x-rapidapi-key': key
    }

    def __init__(self, city):
        self.city = city.title() if city else my_city
        self.query = {
            "lang": "ru",
            "units": "\"metric\"",
            "mode": "json",
            "q": self.city
        }
        self.weather_forecast()

    def weather_forecast(self):
        """
        Создает запрос на внешний API и сохраняет необходимые данные
        в атрибуте self.city_forecast, в случае ошибок сохраняет текст
        ошибки в файле 'city_log.txt'
        :return: None
        """
        try:
            response = requests.request("GET", CityInfo.url,
                                        headers=CityInfo.headers,
                                        params=self.query).json()
        except requests.RequestException as ex:
            self.city_forecast = 'Ошибка соединения с сервером'
            with open('city_log.txt', 'w') as log_file:
                log_file.write(str(ex))
        else:
            if str(response['cod'])[0] == '2':
                self.city_forecast = {
                    'Город': self.city,
                    'Температура': f'{int(response["main"]["temp"] - 273.15)} °C',
                    'На улице': response['weather'][0]['description'],
                    'Скорость ветра': f'{response["wind"]["speed"]} м/с'
                }  # API Возвращает температуру в кедьвинах, поэтому её
                # необходимо переводить в граддусы цельсия
            else:
                self.city_forecast = 'Неверно введен город'

    def __str__(self):
        """
        Если ошибок не было, то итерируется по словарю и переводит
        необходимые данные в строковой формат, в противном случае
        возвращает строку для пользователя с типом ошибки
        """
        if type(self.city_forecast) is dict:
            res_string = ''
            for key, val in self.city_forecast.items():
                res_string += f'{key}: {val}\n'
        else:
            res_string = self.city_forecast
        return res_string


def main():
    city = input('Enter the city: ')  # также можно использовать аргументы
    # командной строки, но мне так удобней
    city_info = CityInfo(city)
    print(city_info)


if __name__ == '__main__':
    main()
