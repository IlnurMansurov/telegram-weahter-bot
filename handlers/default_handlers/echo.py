from telebot.types import Message

from loader import bot



@bot.message_handler(state=None)
def bot_echo(message: Message) -> None:
    """
    Эхо хендлер, куда летят текстовые сообщения без указанного состояния

    :param message: Объект сообщения от Telegram API.
    :type message: telebot.types.Message
    :return: Функция ничего не возвращает.
    :rtype: None
    """
    bot.reply_to(
        message, "Эхо без состояния или фильтра.\n" f"Сообщение: {message.text}"
    )
