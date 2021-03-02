import telebot
import random
# import string

global questions_list
with open('grin_questions.csv', 'r', encoding='utf-8') as f:
    questions_list = f.read()

questions_list = questions_list.split('\n')
random.shuffle(questions_list)
questions_list = [c.split(';') for c in questions_list]

token = '1576012965:AAGdavZE7eLE_JlMgL9b9e0bCSh77hlZYDM'
users = {}

msgs_for_ranswer = ['Отлично! Это правильный ответ\nА вот это знаешь?',
'Да вы хорошо знаете Лесю, дайте виртуальное пять!\nСледующий вопрос',
'Верно!\nИдем дальше']

wanswer_pattern = 'Чтобы продолжить получать вопросы, вашей команде нужно записать видео и отправить мне сюда!'

msgs_for_wanswer = [
f'''Упсики.. это неправильный ответ.
{wanswer_pattern}
Пусть каждый участник команды назовет по одному слову, которое описывает Лесю лучше всего!
Длина видео не больше 1,5 минут!''',
f'''Ой..а вы ошиблись:)
{wanswer_pattern}

Всей команде нужно изобразить серферов на Баренцовом море!
Длина видео не больше 1 минуты!"''',
f'''
Неа, это неправильный ответ!
{wanswer_pattern}

Всей команде нужно изобразить отчаившихся зимбабвийских шаманов вызвать дождь на дуэль!
Длина видео не больше 1 минуты!''',
f'''Ой..а вы ошиблись:)
{wanswer_pattern}

Всей команде нужно изобразить папуасов из Новой Гвинеи, которые впервые увидели белого человека!
Длина видео не больше 1 минуты!''',
f'''Упсики.. это неправильный ответ.
{wanswer_pattern}

Пусть каждый участник команды чего-то пожелает Лесе в трех словах!
Длина видео не больше 1,5 минуты!''',
f'''Неа, это неправильный ответ!
{wanswer_pattern}

Пусть каждый участник команды кратко поделится впечатлением сегодняшнего дня!
Длина видео не больше 1,5 минуты!''',
f'''Неа, это неправильный ответ!
{wanswer_pattern}

Всей команде нужно станцевать сиртаки!
Длина видео не больше 1 минуты!'''
]
random.shuffle(msgs_for_wanswer)

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.questions = questions_list[:]
        random.shuffle(self.questions)
        self.right_answer = ''
        self.right_answers = 0
        self.wait_video = False
        self.go = False
        # self.wanswers = msgs_for_wanswer[:]
        # random.shuffle(self.wanswers)
        self.ranswers = msgs_for_ranswer[:]
        random.shuffle(self.ranswers)

    def get_answer(self, how_answer):
        if how_answer == 'r':
            response = self.ranswers.pop()
            self.ranswers.insert(0, response)
        else:
            response = msgs_for_wanswer.pop()
            msgs_for_wanswer.insert(0, response)
        return response

    def __eq__(self, other):
        if self.user_id == other:
            return True
        else:
            return False

bot = telebot.TeleBot(token)

def make_keyboard(right_answer, user_questions_list):
    answers_list = right_answer
    # pos_list = [x for x in range(len(user_questions_list)-1)]
    # for i in range(3):
    #     answers_list.append(user_questions_list[random.choice(pos_list)][1])
    random.shuffle(answers_list)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(answers_list[0], answers_list[1])
    keyboard.row(answers_list[2], answers_list[3])
    return keyboard

# def code_generator():
#     letters = string.ascii_uppercase
#     rand_string = ''.join(random.choice(letters) for i in range(10))
#     return rand_string

def ask_quistion(message):
    if users[message.chat.id].right_answers < 4:
        # random.shuffle(users[message.chat.id].questions)
        hook_question = users[message.chat.id].questions.pop()
        question, answer = hook_question[0], hook_question[1:5]
        users[message.chat.id].right_answer = answer[0]
        bot.send_message(message.chat.id, f'{question}', reply_markup=make_keyboard(answer, users[message.chat.id].questions))
    else:
        # secret_code = code_generator()
        bot.send_message(message.chat.id, f'Поздравляю! Вы справились! Ваши координаты 43.418412, 39.924003')
        bot.send_message('-512457793', f'Для {message.from_user.first_name} код получен')


@bot.message_handler(commands=['reset'])
def reset_message(message):
    global users
    users = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.id not in users:
        users[message.chat.id] = User(message.chat.id)
    if not users[message.chat.id].go:
        bot.send_message(message.chat.id,
        f'''Приветствую! Тут вас ждет небольшая викторина по фактам из жизни именинницы!
Пройдете викторину - получите код для движка!
За каждый неверный ответ придется выполнить командное задание, снять его на видео и отправить его мне!
    
Начнем с простого: для запуска викторины напиши /go''')

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
                    bot.send_message(message.chat.id, users[message.chat.id].get_answer('r'))
                    ask_quistion(message)
                    users[message.chat.id].right_answers += 1
                else:
                    bot.send_message(message.chat.id, users[message.chat.id].get_answer('w'))
                    users[message.chat.id].wait_video = True


@bot.message_handler(content_types=['video'])
def return_video(message):
    if message.chat.id in users and users[message.chat.id].wait_video:
        users[message.chat.id].wait_video = False
        users[message.chat.id].right_answers += 1
        bot.send_message(message.chat.id, f'Окей, идём дальше!')
        ask_quistion(message)
        bot.forward_message('-512457793', message.chat.id, message.id)

    else:
        if not users[message.chat.id].go:
            bot.send_message(message.chat.id, f'Для запуска викторины напиши /go')

@bot.message_handler(content_types=['audio','document','photo','sticker','video_note','voice','location','contact','new_chat_members','left_chat_member','new_chat_title','new_chat_photo','delete_chat_photo','group_chat_created','supergroup_chat_created','channel_chat_created','migrate_to_chat_id','migrate_from_chat_id','pinned_message'])
def return_media(message):
    if message.chat.id not in users:
        bot.send_message(message.chat.id, f'Мы как-то пропустили момент со знакомством, пиши /start и я тебя запомню...')
    else:
        if not users[message.chat.id].go:
            bot.send_message(message.chat.id, f'Для запуска викторины напиши /go')
        else:
            if users[message.chat.id].wait_video:
                bot.send_message(message.chat.id, f'Не-не-не, не то, жду видео!')

bot.polling()
