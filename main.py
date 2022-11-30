from aiogram import Bot, Dispatcher, executor, types
import python_weather
import datetime
import asyncio
import os
import re

# bot init

bot = Bot(token="5709842033:AAGVdn0O4nRwnKSTfe2LsfQodlHz5ro5LlU")
dp = Dispatcher(bot)
# async with python_weather.Client(format=python_weather.IMPERIAL) as client
client = python_weather.Client(format=python_weather.IMPERIAL)
# echo
@dp.message_handler()
async def echo(massage: types.Message):
    weather = await client.get(massage.text)
    weather.format = "C"
    response = ""
    w_location = str(weather.location).replace('(', '').replace(')', '')
    if massage.text == '/start' :
        response = f"Приветствую, {massage.from_user.full_name}!🤚🏻\n" \
                   f"Я - тестовый бот, который скажет тебе погоду😊\n" \
                   f"Напиши мне город и я отвечу 😉"
    else:
        response = f"Погода в городе {weather.nearest_area.name}, {weather.nearest_area.region}, {weather.nearest_area.country} \n" \
               f"на момент {weather.current.local_time.date()}, {weather.current.local_time.time()}:\n\n" \
               f"Погода: {weather.current.description}\n" \
               f"Осадки: {weather.current.precipitation} мм.\n" \
               f"Температура: {str(weather.current.temperature)} °C\n" \
               f"Ветер: {weather.current.wind_direction}, скорость: {round(weather.current.wind_speed*0.44704)} м/с\n" \
               f"Влажность воздуха: {weather.current.humidity} %\n"

    log_note = f"user_id: {massage.from_user.id}, user_full_name: {massage.from_user.full_name}, user_name: {massage.from_user.username}, user_is_bot: {massage.from_user.is_bot} " \
               f"send message {massage.message_id} in chat {massage.chat.id} в {massage.date}: {massage.text}"
    print(log_note)
    print(f"RESPONSE: {response}")
    await massage.answer(response)

# run long-polling
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
