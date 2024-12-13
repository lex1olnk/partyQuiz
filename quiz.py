from telebot import types
from questions import questions  # Импортируем вопросы

def start_quiz(message, bot, users_data):
    # Проверяем, существует ли пользователь в данных
    if message.chat.id not in users_data: 
        # Если нет, создаем новую запись для пользователя
        users_data[message.chat.id] = { 
            "answers": [0 for i in range(len(questions))], 
            "user_name": message.from_user.first_name or message.from_user.username or message.chat.first_name or "nobody", 
            "final_score": 0, 
            "current_index": 0, 
        } 
    
    # Обнуляем баллы и индекс для текущего пользователя
    users_data[message.chat.id]["final_score"] = 0 
    users_data[message.chat.id]["current_index"] = 0
    send_question(message, bot, users_data)


def send_question(message, bot, users_data):
    question_index = users_data[message.chat.id]["current_index"]
    
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
        item = types.KeyboardButton("Посмотреть на мои ответы")
        item2 = types.KeyboardButton("Все результаты")
        markup.add(item)
        markup.add(item2)
        bot.send_message(message.chat.id, f'Спасибо за участие в опросе! Ваш результат: {users_data[message.chat.id]["final_score"]} из {len(questions)}', reply_markup=markup)


def handle_answer(message, bot, users_data):
    question_index = users_data[message.chat.id]["current_index"]
    users_data[message.chat.id]["answers"][question_index] = questions[question_index]["options"].index(message.text)
    if questions[question_index]["options"].index(message.text) == questions[question_index]["correct_answer"]:
        users_data[message.chat.id]["final_score"] += 1
    
    users_data[message.chat.id]["current_index"] += 1
    send_question(message, bot, users_data)


def show_user_answers(message, bot, users_data):
    #question_index = user_question_index[message.chat.id]
    for i in range(len(users_data[message.chat.id]["answers"])):
        answer_text = questions[i]["options"][users_data[message.chat.id]["answers"][i]]
        answer = []
        answer.append(f'Вопрос № {i + 1}')
        answer.append(f'{questions[i]["question"]} - {questions[i]["options"][questions[i]["correct_answer"]]}')
        answer.append(f'Мой ответ: {answer_text}')
        bot.send_message(message.chat.id, '\n'.join(answer))
    
    bot.send_message(message.chat.id, f'Спасибо за участие в опросе! Ваш результат: {users_data[message.chat.id]["final_score"]} из {len(questions)}')


def show_all_answers(message, bot, users_data):
    users = []
    for chat_id in users_data:
        users.append(f'{users_data[chat_id]['user_name']} набрал(а) {users_data[chat_id]['final_score']} очков')
    index = max(users_data, key=lambda x: users_data[x]['final_score'])
    
    bot.send_message(message.chat.id, '\n'.join(users))
    bot.send_message(message.chat.id, f'В данный момент лидирует {users_data[index]['user_name']} c {users_data[index]['final_score']} очками')
