import telebot
import random
import string

global questions_list
with open('Quistions.csv', 'r') as f:
    questions_list = f.read()
questions_list = questions_list.split('\n')
random.shuffle(questions_list)
questions_list = [c.split(';') for c in questions_list]
questions_list.pop()

token = '1576012965:AAGdavZE7eLE_JlMgL9b9e0bCSh77hlZYDM'
users = {}

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.questions = questions_list[:]
        self.right_answer = ''
        self.right_answers = 0
        self.wait_video = False
        self.go = False

    def __eq__(self, other):
        if self.user_id == other:
            return True
        else:
            return False

bot = telebot.TeleBot(token)

def make_keyboard(right_answer, user_questions_list):
    answers_list = [right_answer]
    pos_list = [x for x in range(len(user_questions_list)-1)]
    for i in range(3):
        answers_list.append(user_questions_list[random.choice(pos_list)][1])
    random.shuffle(answers_list)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(answers_list[0], answers_list[1])
    keyboard.row(answers_list[2], answers_list[3])
    return keyboard

def code_generator():
    letters = string.ascii_uppercase
    rand_string = ''.join(random.choice(letters) for i in range(10))
    return rand_string

def ask_quistion(message):
    if users[message.chat.id].right_answers < 4:
        hook_question = users[message.chat.id].questions.pop()
        question, answer = hook_question[0], hook_question[1]
        users[message.chat.id].right_answer = answer
        bot.send_message(message.chat.id, f'Столица страны: {question}', reply_markup=make_keyboard(answer, users[message.chat.id].questions))
    else:
        bot.send_message(message.chat.id, f'А, нет, не идём...')
        secret_code = code_generator()
        bot.send_message(message.chat.id, f'ПОооооОбеда, твой секретный код: {secret_code}, неговори никому!!')
        bot.send_message('-512457793', f'Для {message.from_user.first_name} получен код: {secret_code}')


@bot.message_handler(commands=['reset'])
def reset_message(message):
    global users
    users = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in users:
        users[message.chat.id] = User(message.chat.id)
    bot.send_message(message.chat.id, f'Для запуска викторины напиши /go')

@bot.message_handler(commands=['go'])
def go_message(message):
    if message.chat.id not in users:
        bot.send_message(message.chat.id, f'Мы как-то пропустили момент со знакомством, пиши /start и я тебя запомню...')
    else:
        if not users[message.chat.id].go:
            users[message.chat.id].go = True
            ask_quistion(message)
        else:
            if users[message.chat.id].wait_video:
                bot.send_message(message.chat.id, f'Жду видосик...')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.chat.id not in users:
        bot.send_message(message.chat.id, f'Мы как-то пропустили момент со знакомством, пиши /start и я тебя запомню...')
    else:
        if not users[message.chat.id].go:
            bot.send_message(message.chat.id, f'Для запуска викторины напиши /go')
        else:
            if users[message.chat.id].wait_video:
                bot.send_message(message.chat.id, f'Жду видосик...')
            else:
                if message.text.lower() == users[message.chat.id].right_answer.lower():
                    bot.send_message(message.chat.id, 'Это Правильный ответ!!!')
                    bot.send_message(message.chat.id, 'Идём дальше...')
                    ask_quistion(message)
                    users[message.chat.id].right_answers += 1
                else:
                    bot.send_message(message.chat.id, 'Это НЕ правильный ответ')
                    bot.send_message(message.chat.id, f'Это ПроВаЛ(((')
                    bot.send_message(message.chat.id, f'С тебя видосик!)')
                    users[message.chat.id].wait_video = True


@bot.message_handler(content_types=['video'])
def return_media(message):
    if message.chat.id in users and users[message.chat.id].wait_video:
        users[message.chat.id].wait_video = False
        users[message.chat.id].right_answers += 1
        ask_quistion(message)
        bot.forward_message('-512457793', message.chat.id, message.id)

    else:
        if not users[message.chat.id].go:
            bot.send_message(message.chat.id, f'Для запуска викторины напиши /go')


bot.polling()
