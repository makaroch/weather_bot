import telebot
import requests
from sourse import MY_TOKEN, API_KEY
from weather import get_weather, WeatherException

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

@bot.message_handler(commands=["information"])
def information(message):
    bot.send_message(message.chat.id, f"1. ключ: `{API_KEY}` \n"
                                      f"2. документация: [https://openweathermap.org/current](https://openweathermap.org/current)\n"
                                      f"3. установка requests: `pip install requests`\n"
                                      f"4. установка telebot: `pip install pyTelegramBotAPI`", parse_mode="MARKDOWN")


@bot.message_handler(content_types=['text'])
def send_text(message):
    write_weather(message)


def write_weather(message):
    text_weather: str = ""
    try:
        text_weather = get_weather(message.text)
    except WeatherException as e:
        text_weather = str(e)
    except Exception as e:
        print(e)
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
