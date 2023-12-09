from typing import Tuple
from sourse import *
import requests

UNITS = "metric"


class WeatherException(Exception):
    pass


def get_lat_lon_city(city: str) -> Tuple[str, str]:
    req_coord = f"http://api.openweathermap.org/geo/1.0/direct?q={city},ru&limit=5&appid={API_KEY}"
    data_city = requests.get(req_coord).json()

    if len(data_city) == 0:
        raise WeatherException("Неверно указан город!")

    data_city = data_city[-1]

    lat_city = data_city["lat"]
    lon_city = data_city['lon']
    print(lat_city, lon_city)
    return lat_city, lon_city


def get_weather(city):
    lat, lon = get_lat_lon_city(city)

    req = (f"https://api.openweathermap.org/data/2.5/weather?lat={lat}"
           f"&lon={lon}&appid={API_KEY}&lang=ru&units={UNITS}")
    x = requests.get(req)
    weather_json = x.json()

    wind_speed = weather_json["wind"]["speed"]
    weather_short: str = weather_json["weather"][0]["description"]
    weather_main = weather_json["main"]
    temp = weather_main["temp"]
    temp_max = weather_main["temp_max"]
    temp_min = weather_main["temp_min"]
    feels_like = weather_main["feels_like"]
    return (
        f"<b><i>{weather_short.title()}</i></b>, текущая температура: <i>{temp}℃</i>\nПо ощущениям: <i>{feels_like}℃</i>\n"
        f"Максимальная за сегодня: <i>{temp_max}℃</i>\nМинимальная за сегодня: <i>{temp_min}℃</i>\nСкорость ветра: <i>{wind_speed}м/с</i>")
