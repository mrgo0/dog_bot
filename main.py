import telebot
from telebot import types
import requests
import random
from translate import Translator


API_TOKEN = '6569910994:AAFMZfIHqNJaVoBEKn0Qz4Ngc0UN5H0y9Dc'

bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Введите название породы собаки, чтобы я прислал фотографию")


@bot.message_handler(content_types=['text'])
def get_breed(message):
    translator = Translator(from_lang="russian", to_lang="english")
    dog_breed = message.text.lower()
    dog_breed = translator.translate(dog_breed).lower()
    url = f'https://dog.ceo/api/breed/{dog_breed}/images/random'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'success':
        image = data['message']
        bot.send_photo(message.chat.id, image)
    else:
        bot.reply_to(message, "Извините, не могу найти фотографию этой породы.")


bot.polling(none_stop=True)
