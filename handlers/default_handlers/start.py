from telebot.types import Message
from keyboards.reply.keuboard import kb
from loader import bot
from database.Database import User, db

@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Обработчик команды /start. Создает или получает пользователя из базы данных,
    приветствует его и отправляет клавиатуру с дополнительными командами.

    :param message: Объект сообщения от Telegram API.
    :type message: telebot.types.Message
    """
    with db:
        try:
            user = User.get(User.user_id == message.chat.id)
        except User.DoesNotExist:
            user = User.create(
                username=message.from_user.full_name,
                user_id=message.chat.id
            )
            user.save()

        bot.reply_to(
            message,
            f"Привет, {message.from_user.full_name}!",
            reply_markup=kb
        )




