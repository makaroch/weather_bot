import telebot
import requests
from sourse import MY_TOKEN
from weather import get_weather

bot = telebot.TeleBot(MY_TOKEN)


@bot.message_handler(commands=['dog'])
def welcome(message):
    print(f'{message.from_user.first_name}: {message.chat.id}')
    get_img(message)


@bot.message_handler(commands=['cat'])
def welcome(message):
    print(f'{message.from_user.first_name}: {message.chat.id}')
    get_cat(message)


@bot.message_handler(commands=['start'])
def hello(message):
    print(f'{message.from_user.first_name}: {message.chat.id}')
    bot.send_message(message.chat.id, f"Привет, {message.from_user.first_name} ")


@bot.message_handler(commands=["weather"])
def get_w(message):
    bot.send_message(message.chat.id, "Введите название города")
    bot.register_next_step_handler(message, write_weather)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower().replace(" ", "") == "какойпесельтысегодня?":
        bot.send_message(message.chat.id, "Иии тебе выпал вот <i>такой!!!</i>", parse_mode='html')
        get_img(message)


def write_weather(message):
    try:
        text_weather = get_weather(message.text)
    except Exception as e:
        text_weather = str(e)
    bot.send_message(message.chat.id, text_weather, parse_mode="html")


def get_cat(message):
    req = requests.get("https://api.thecatapi.com/v1/images/search")
    if req.status_code == 200:
        req = req.json()
        bot.send_photo(message.chat.id, req[0]['url'])
    else:
        bot.send_message(message.chat.id, "Тут должен был быть котик, но что-то пошло не так(")


def get_img(message):
    req = requests.get("https://random.dog/woof.json")
    if req.status_code == 200:
        req = req.json()
        bot.send_photo(message.chat.id, req['url'])
    else:
        bot.send_message(message.chat.id, "Тут должен был быть песик, но что-то пошло не так(")


bot.infinity_polling()
