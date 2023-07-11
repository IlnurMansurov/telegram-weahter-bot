from telebot.types import Message

from keyboards.reply.keuboard import kb
from loader import bot
from collections import defaultdict
from  database.Database import Request
user_context = defaultdict(dict)

@bot.message_handler(commands=["history"])
def history(message: Message):
    """
       Обработчик команды /history
       отправляет пользователю результаты последних 10 запросов

       :param message: Объект сообщения от Telegram API.
       :type message: telebot.types.Message

       :return: Функция ничего не возвращает.
       :rtype: None
    """
    user_id = message.chat.id
    requests = Request.select().where(Request.user_id == user_id).limit(10)
    response = "История ваших запросов:\n\n"
    for r in reversed(requests):
        response += f"{r.query}\n"
    bot.reply_to(message, response, reply_markup=kb)
