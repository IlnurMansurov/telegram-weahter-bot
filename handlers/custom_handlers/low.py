from telebot.types import Message

from keyboards.reply.keuboard import kb
from loader import bot
from collections import defaultdict
from database.Database import Request, db
from handlers.custom_handlers.weather import weather,geo
user_context = defaultdict(dict)



@bot.message_handler(commands=["low"])
def bot_start(message: Message):
    """
       Обработчик команды /low.
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

def get_weather(coordinate, message):
    """
       Отправляет пользователю погоду на сегодняшний день
       сохраняет результаты запросов в базу данных.

       :param message: Объект сообщения от Telegram API.
       :type message: telebot.types.Message
       :param coordinate: Координаты населенного пункта по широте и долготе.
       :type coordinate: Str
       :param date_list: Список доступных дат для прогноза.
       :type date_list: List

       :return: Функция ничего не возвращает.
       :rtype: None
       """
    user_id = message.chat.id
    message_text = weather(coordinate)
    if message_text:
        bot.send_message(user_id, message_text, reply_markup=kb)
        with db:
            request = Request(user=user_id, query=message_text)
            request.save()
    else:
        bot.send_message(user_id, 'К сожалению ничего не найдено', reply_markup=kb)





