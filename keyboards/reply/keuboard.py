from telebot import types
from typing import List
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def bot_markup(list_: List[str]) -> ReplyKeyboardMarkup:
    """
    Создает и возвращает ReplyKeyboardMarkup с кнопками, заданными в list_.

    :param list_: Список строк с названиями кнопок.
    :type list_: List[str]

    :return: ReplyKeyboardMarkup c добавленными кнопками.
    :rtype: telebot.types.ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for elem in list_:
        btn = KeyboardButton(elem)
        markup.add(btn)
    return markup


# Клавиатура со стандартными командами бота
kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
low = types.KeyboardButton(text='/low')
high = types.KeyboardButton(text='/high')
custom = types.KeyboardButton(text='/custom')
history = types.KeyboardButton(text='/history')
help = types.KeyboardButton(text='/help')
kb.add(low, high, custom, history, help)
