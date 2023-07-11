from telebot.types import Message
from keyboards.reply.keuboard import kb
from loader import bot
from collections import defaultdict
from database.Database import Request, db
from handlers.custom_handlers.weather import weather, geo
import datetime
user_context = defaultdict(dict)


@bot.message_handler(commands=["high"])
def bot_start(message: Message) -> None:
    """
    Обработчик команды /high.
    Запрашивает у пользователя название населенного пункта
    переадресовывает на функцию geo

    :param message: Объект сообщения от Telegram API.
    :type message: telebot.types.Message

    :return: Функция ничего не возвращает.
    :rtype: None
    """
    user_id = message.chat.id
    user_context[user_id]["command"] = message.text
    bot.reply_to(message, f"Укажите название населенного пункта:")
    bot.register_next_step_handler(message, geo(get_weather))


def get_weather(coordinate: str, message: Message) -> None:
    """
    Отправляет пользователю погоду на неделю
    сохраняет результаты запросов в базу данных.

    :param message: Объект сообщения от Telegram API.
    :type message: telebot.types.Message
    :param coordinate: Координаты населенного пункта по широте и долготе.
    :type coordinate: Str

    :return: Функция ничего не возвращает.
    :rtype: None
    """
    user_id = message.chat.id
    message_text = weather(coordinate)
    if message_text:
        with db:
            request = Request(user=user_id, query=message_text)
            request.save()
        now = datetime.datetime.now().date()
        for i in range(1, 7):
            day = (now + datetime.timedelta(days=i))
            with db:
                request = Request(user=user_id, query=day)
                request.save()
            message_text += weather(coordinate=coordinate, weather_date=day)
        bot.send_message(user_id, message_text, reply_markup=kb)
    else:
        bot.send_message(user_id, 'К сожалению ничего не найдено', reply_markup=kb)



