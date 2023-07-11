import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()
DATABASE = 'telegram_bot.db'
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("low", "Запрос погоды на сегодня"),
    ("history", "Результаты последних 10 запросов"),
    ("high", "Запрос погоды на неделю"),
    ("custom", "Запрос погоды на нужные даты")
)

