import requests
import json
from config_data.config import RAPID_API_KEY
from datetime import date
from telebot.types import Message
from typing import Any, Callable

from keyboards.reply.keuboard import bot_markup, kb
from loader import bot


def weather(coordinate: str, weather_date: date = date.today()) -> Any:
    """
    Получает погоду по координатам на определенную дату
    по умолчанию текущая дата
    :param coordinate: координаты населенного пункта
    :param weather_date: дата
    :return: текст с погодой
    """
    url = "https://weatherapi-com.p.rapidapi.com/forecast.json"
    querystring = {"q": coordinate, 'lang': 'ru', 'dt': weather_date}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        weather = json.loads(response.text)

        message_text = f"{weather['location']['name']}, {weather['location']['region']}, " \
                       f"{weather['location']['country']}\n{weather['forecast']['forecastday'][0]['date']}\n Максимальная температура днём: " \
                       f"{weather['forecast']['forecastday'][0]['day']['maxtemp_c']}°C, ночью до: {weather['forecast']['forecastday'][0]['day']['mintemp_c']}°C\nВетер до " \
                       f"{weather['forecast']['forecastday'][0]['day']['maxwind_mph']} метров в час\n\n"
        return message_text

    else:
        return None




def geo(func: Callable[..., Any]) -> Callable[[Message], None]:
    """
    Декоратор для функций бота получающий координаты населенного пункта.

    :param func: Функция, которую нужно декорировать.
    :type func: Callable[..., Any]

    :return: Обернутая декоратором функция.
    :rtype: Callable[[Message], None]
    """

    def wrapper(message: Message) -> None:
        """
        Получает координаты населенного пункта с помощью TrueWay Geocoding API.
        Вызывает функцию, переданную в декораторе, с параметрами message и coordinate.

        :param message: Объект сообщения от Telegram API.
        :type message: telebot.types.Message

        :return: Функция ничего не возвращает.
        :rtype: None
        """
        address = message.text
        url = "https://trueway-geocoding.p.rapidapi.com/Geocode"
        querystring = {"address": address, "language": "ru"}
        headers = {
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "trueway-geocoding.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        result = json.loads(response.text)

        if response.status_code == 200 and result['results']:
            if len(result['results']) == 1:
                lat = result['results'][0]['location']['lat']
                lng = result['results'][0]['location']['lng']
                coordinate = f"{lat},{lng}"
                func(message=message, coordinate=coordinate)
            else:
                address_list = [result['results'][i]['address'] for i in range(len(result['results']))]
                bot.send_message(
                    message.from_user.id,
                    'Уточните, пожалуйста:',
                    reply_markup=bot_markup(address_list)
                )
                bot.register_next_step_handler(message, geo_coordinate, func, result, address_list)
        else:
            bot.reply_to(message, 'К сожалению ничего не найдено')

    return wrapper


def geo_coordinate(message: Message, func: Callable[..., Any], result: dict, address_list: list) -> None:
    """
    Получает координаты, и продолжает выполнение оригинальной функции
    вызывает переданную функцию с параметрами message и coordinate.

    :param message: Объект сообщения от Telegram API.
    :type message: telebot.types.Message

    :param func: Оригинальная функция.
    :type func: Callable[..., Any]

    :param result: Результат запроса к API геокодинга
    :type result: Dict

    :param address_list: Список адресов.
    :type address_list: List

    :return: Функция ничего не возвращает.
    :rtype: None
    """

    if message.text in address_list:
        for i in range(len(result['results'])):
            if result['results'][i]['address'] == message.text:
                lat = result['results'][i]['location']['lat']
                lng = result['results'][i]['location']['lng']
                coordinate = f"{lat},{lng}"
                func(message=message, coordinate=coordinate)
    else:
        bot.send_message(message.from_user.id, 'Неверно указан адрес:', reply_markup=kb)
