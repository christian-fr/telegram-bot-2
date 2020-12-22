# https://blog.seamlesscloud.io/2020/09/be-prepared-for-bad-weather-using-20-lines-of-python/


# icons rendering - kindleb
# https://mpetroff.net/2012/09/kindle-weather-display/

import os

import requests

api_file = '/home/christian/PycharmProjects/telegram-bot/weather_forecast/openweather_api_key.txt'
#WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
with open(api_file, 'r') as f:
    WEATHER_API_KEY = f.read()
LATITUDE = os.getenv('LATITUDE')
LONGITUDE = os.getenv('LONGhttps://blog.seamlesscloud.io/2020/09/be-prepared-for-bad-weather-using-20-lines-of-python/ITUDE')
BOT_API_KEY = os.getenv('BOT_API_KEY')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')
import os

import requests

CITY_ID = '2910831'

if __name__ == '__main__':
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/forecast/hourly?id={CITY_ID}&appid={WEATHER_API_KEY}')
        
    # f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&APPID={WEATHER_API_KEY}")

if __name__ == '__main__':
    resp = requests.get(
        f"https://api.openweathermap.org/data/2.5/onecall?lat={LATITUDE}&lon={LONGITUDE}&APPID={WEATHER_API_KEY}")
    forecast = resp.json()['daily'][0]
    today_weather = forecast['weather'][0]['description']
    if 'rain' in today_weather:
        requests.get(f'https://api.telegram.org/bot{BOT_API_KEY}/sendMessage',
                     params={'chat_id': CHANNEL_NAME,
                             'text': 'It\'s going to rain today' + u'\U00002614' + ', take your umbrella with you!'})