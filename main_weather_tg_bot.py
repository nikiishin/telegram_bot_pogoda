import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю тебе сводку погоды!")

@dp.message_handler()
async def get_wather(message: types.Message):
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
            f"https://api.openweathermap.org//data//2.5//weather?q={message.text}&appid={open_weather_token}&units=metric"
            # 4.ищем ссылку api с городом и два параметра город и ключ
        )
        data = r.json()  # 5.записываем в json
        # pprint(data)

        city = data["name"]  # обращаемся к ключу name чтобы получить название города
        cur_waether = data["main"]["temp"]  # находим текущую погода по ключу main temp
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
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        await message.reply(f"*** {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')} ***\n"
              f"Погода в городе: {city}\nТемпература: {cur_waether}C° {wd}\n"
              f"Влажность: {cur_humidity}%\nДавление: {cur_pressure} мм.рт.ст\n"
              f"Ветер: {wind} м/с\nВосход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
              f"Продолжительность дня: {length_of_the_day}\n"
              f"***Хорошего дня!***\n")



    except:

        await message.reply("\U00002620 Проверьте название города \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)