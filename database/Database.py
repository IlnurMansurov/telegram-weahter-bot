import telebot
import peewee
from config_data.config import DATABASE
# создание объекта бота с вашим токеном
bot = telebot.TeleBot("TOKEN")

# подключение к базе данных SQLite
db = peewee.SqliteDatabase(DATABASE)


# определение модели пользователя
class User(peewee.Model):
    username = peewee.CharField(max_length=50, null=True, unique=True)
    user_id = peewee.IntegerField(unique=True)

    class Meta:
        database = db


# определение модели истории запросов
class Request(peewee.Model):
    user = peewee.ForeignKeyField(User, backref='requests')
    query = peewee.TextField()

    class Meta:
        database = db
        order_by = ('-id',)


# создание таблиц в базе данных
User.create_table()
Request.create_table()



