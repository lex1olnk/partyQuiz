import telebot
from telebot import types
from questions import questions  # Импортируем вопросы

user_score = {}

def start_quiz(message, bot, user_question_index):
    user_question_index[message.chat.id] = 0
    user_score[message.chat.id] = 0
    send_question(message, bot, user_question_index)

def send_question(message, bot, user_question_index):
    question_index = user_question_index[message.chat.id]
    
    if question_index < len(questions):
        question_data = questions[question_index]
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        for option in question_data["options"]:
            markup.add(types.KeyboardButton(option))
        
        #if question_data["image"]:
        #    bot.send_photo(message.chat.id, question_data["image"])

        if question_data["image"]: 
            with open(question_data["image"], 'rb') as img_file:
                bot.send_photo(message.chat.id, img_file) 

        bot.send_message(message.chat.id, question_data["question"], reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item = types.KeyboardButton("Посмотреть на результаты")
        markup.add(item)
        bot.send_message(message.chat.id, f'Спасибо за участие в опросе! Ваш результат: {user_score[message.chat.id]} из {len(questions)}', reply_markup=markup)


def handle_answer(message, bot, user_question_index):
    question_index = user_question_index[message.chat.id]
    
    if questions[question_index]["options"].index(message.text) == questions[question_index]["correct_answer"]:
        user_score[message.chat.id] += 1
    
    user_question_index[message.chat.id] += 1
    send_question(message, bot, user_question_index)


def handle_ending(message, bot, user_question_index):
    #question_index = user_question_index[message.chat.id]
    bot.send_message(message.chat.id, f'Спасибо за участие в опросе! Ваш результат: {user_score[message.chat.id]} из {len(questions)}')

