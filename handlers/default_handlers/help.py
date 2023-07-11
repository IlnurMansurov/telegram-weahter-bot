from telebot.types import Message

from config_data.config import DEFAULT_COMMANDS
from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message) -> None:
    """
       Обработчик команды /help
       отправляет пользователю доступные команды бота

       :param message: Объект сообщения от Telegram API.
       :type message: telebot.types.Message

       :return: Функция ничего не возвращает.
       :rtype: None
    """
    text = [f"/{command} - {desk}" for command, desk in DEFAULT_COMMANDS]
    bot.reply_to(message, "\n".join(text))
