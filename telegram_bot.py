# 1.получаем токен на openn weather сохраняем ключ в файле config
import datetime

import requests
#6 импортируем что бы красиво разложить по полочкам json файл
from pprint import pprint

from config import open_weather_token   # 2.импортируем файл config

# 3. Импортируем библиатеку requests

def get_weather(city, open_weather_token):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"

    }
    try:
        r = requests.get(
            f"https://api.openweathermap.org//data//2.5//weather?q={city}&appid={open_weather_token}&units=metric"  #4.ищем ссылку api с городом и два параметра город и ключ
        )
        data = r.json() #5.записываем в json
        # pprint(data)

        city = data["name"] #обращаемся к ключу name чтобы получить название города
        cur_waether = data["main"]["temp"] #находим текущую погода по ключу main temp
        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"
        cur_humidity = data["main"]["humidity"]
        cur_pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        print(f"*** {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')} ***\n"
            f"Погода в городе: {city}\nТемпература: {cur_waether}C° {wd}\n"
              f"Влажность: {cur_humidity}%\nДавление: {cur_pressure} мм.рт.ст\n"
              f"Ветер: {wind} м/с\nВосход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
              f"Продолжительность дня: {length_of_the_day}\n"
              f"Хорошего дня!")

    except Exception as ex:
        print(ex)
        print("Проверьте название города")

def main():
    city = input("Введите город:")
    get_weather(city, open_weather_token)

if __name__ == '__main__':
    main()


#что бы перенести в телеграм устанавливаем библиотеку aiogram