import telebot
import os
from telebot import types
from quiz import start_quiz, handle_answer, handle_ending
from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
user_question_index = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item = types.KeyboardButton("Старт")
    markup.add(item)
    bot.send_message(message.chat.id, 'Привет! Нажми на кнопку ниже, чтобы начать:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Старт")
def start_quiz_handler(message):
    start_quiz(message, bot, user_question_index)


@bot.message_handler(func=lambda message: message.text == "Посмотреть на результаты")
def show_quiz_results(message):
    handle_ending(message, bot, user_question_index)


@bot.message_handler(func=lambda message: message.chat.id in user_question_index)
def answer_handler(message):
    handle_answer(message, bot, user_question_index)


bot.infinity_polling()
