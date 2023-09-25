import telebot
import requests
from deep_translator import GoogleTranslator


TOKEN = 'YOUR_TOKEN'
bot = telebot.TeleBot(TOKEN)


# Приветствие
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне название породы собаки, фотографию которой хочешь увидеть")


# Небольшая подсказска
@bot.message_handler(commands=['help'])
def send_help_message(message):
    if message.text == '/help':
        bot.reply_to(message, "/start - начать общение с ботом ")

# Получаем породу собаки, переводим ее с русского на английский язык, получаем случайную фотографию по породе
@bot.message_handler(content_types=['text'])
def get_breed(message):
    translator = GoogleTranslator(source='ru', target='en')
    dog_breed = message.text
    dog_breed = translator.translate(dog_breed).lower()
    if len(dog_breed.split()) == 2:
        first, second = dog_breed.split()
        url = f'https://dog.ceo/api/breed/{second}/{first}/images/random'
    else:
        url = f'https://dog.ceo/api/breed/{dog_breed}/images/random'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 'success':
        image = data['message']
        bot.send_photo(message.chat.id, image)
    else:
        bot.reply_to(message, "Извините, не могу найти фотографию этой породы.")


bot.polling(none_stop=True)

