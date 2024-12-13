import telebot
import os
from telebot import types
from quiz import start_quiz, handle_answer, show_user_answers, show_all_answers
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)


users_data = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Старт")
    markup.add(item)
    bot.send_message(message.chat.id, 'Привет! Нажми на кнопку ниже, чтобы начать:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Старт")
def start_quiz_handler(message):
    start_quiz(message, bot, users_data)


@bot.message_handler(func=lambda message: message.text == "Посмотреть на мои ответы")
def show_user_answers_handler(message):
    show_user_answers(message, bot, users_data)


@bot.message_handler(func=lambda message: message.text == "Все результаты")
def show_all_answers_handler(message):
    show_all_answers(message, bot, users_data)


@bot.message_handler(func=lambda message: message.chat.id in users_data)
def answer_handler(message):
    handle_answer(message, bot, users_data)


bot.infinity_polling()
