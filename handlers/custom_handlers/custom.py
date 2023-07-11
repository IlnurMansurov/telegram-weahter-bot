from telebot.types import Message
from keyboards.reply.keuboard import bot_markup, kb
from loader import bot
from collections import defaultdict
from database.Database import Request, db
from handlers.custom_handlers.weather import weather, geo
import datetime

user_context = defaultdict(dict)

@bot.message_handler(commands=["custom"])
def bot_start(message: Message) -> None:
    """
    Обработчик команды /custom.
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
    bot.register_next_step_handler(message, geo(get_date))


def get_date(message: Message, coordinate: str) -> None:
    """
    Создает список с доступными датами для прогноза
    отправляет пользователю клавиатуру с вариантами ответа
    переадресовывает на функцию first_day

    :param message: Объект сообщения от Telegram API.
    :type message: telebot.types.Message
    :param coordinate: Координаты населенного пункта по широте и долготе.
    :type coordinate: Str

    :return: Функция ничего не возвращает.
    :rtype: None
    """
    date_list = []
    user_id = message.chat.id
    # получаем даты 14 будущих дней
    now = datetime.datetime.now().date()
    for i in range(15):
        day = (now + datetime.timedelta(days=i))
        date_list.append(str(day))

    bot.send_message(message.from_user.id, 'Выберите начало периода:', reply_markup=bot_markup(date_list))
    bot.register_next_step_handler(message, first_day, coordinate=coordinate, date_list=date_list)


def first_day(message: Message, coordinate: str, date_list: list) -> None:
    """
    Получает от пользователя дату начала периода и переадресовывает на функцию get_weather.

    :param message: Объект сообщения от Telegram API.
    :type message: telebot.types.Message
    :param coordinate: Координаты населенного пункта по широте и долготе.
    :type coordinate: Str
    :param date_list: Список доступных дат для прогноза.
    :type date_list: List

    :return: Функция ничего не возвращает.
    :rtype: None
    """

    if message.text in date_list:
        user_date = find_date(lst=date_list, target=message.text)
        bot.send_message(message.from_user.id, 'Выберите окончание периода:', reply_markup=bot_markup(user_date))
        bot.register_next_step_handler(message, get_weather, coordinate=coordinate, date_list=user_date)
    else:
        bot.reply_to(message, f"Неверный формат даты")


def get_weather(message: Message, coordinate: str, date_list: list) -> None:
    """
    Отправляет пользователю погоду на выбранные даты
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

    if message.text in date_list:
        user_id = message.chat.id
        message_text = weather(coordinate=coordinate, weather_date=date_list[0])
        if message_text:
            with db:
                request = Request(user=user_id, query=message_text)
                request.save()

            for elem in date_list[1:]:
                day_weather = weather(coordinate=coordinate, weather_date=elem)
                with db:
                    request = Request(user=user_id, query=day_weather)
                    request.save()
                if elem == message.text:
                    break
                message_text += day_weather
            bot.reply_to(message, message_text, reply_markup=kb)
        else:
            bot.send_message(user_id, 'К сожалению ничего не найдено', reply_markup=kb)
    else:
        bot.send_message(message, 'Неверный формат даты', reply_markup=kb)


def find_date(lst: list, target: str) -> list:
    """
    Находит элемент в списке, и возвращает список начиная с этого элемента.

    :param lst: Список.
    :type lst: List
    :param target: Элемент для поиска.
    :type target: Str

    :return: Список элементов, начиная с искомого.
    :rtype: List
    """
    index = lst.index(target)
    return lst[index:]

