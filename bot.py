import telebot
import random

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


def make_keyboard(right_answer):
    answers_list = right_answer
    random.shuffle(answers_list)
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row(answers_list[0], answers_list[1])
    keyboard.row(answers_list[2], answers_list[3])
    return keyboard


def ask_quistion(message):
    if users[message.chat.id].right_answers < 4:
        hook_question = users[message.chat.id].questions.pop()
        question, answer = hook_question[0], hook_question[1:5]
        users[message.chat.id].right_answer = answer[0]
        bot.send_message(message.chat.id, f'{question}', reply_markup=make_keyboard(answer))
    else:
        bot.send_message(message.chat.id, f'Поздравляю! Вы справились! Ваш код для движка - Победа')
        bot.send_message('-1001177320853', f'Для {message.from_user.first_name} код получен')


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
        bot.send_message(message.chat.id,
                         f'Мы как-то пропустили момент со знакомством, пиши /start и я тебя запомню...')
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
        bot.send_message(message.chat.id,
                         f'Мы как-то пропустили момент со знакомством, пиши /start и я тебя запомню...')
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
    if message.chat.id not in users:
        bot.send_message(message.chat.id,
                         f'Мы как-то пропустили момент со знакомством, пиши /start и я тебя запомню...')
        return
    if message.chat.id in users and users[message.chat.id].wait_video:
        users[message.chat.id].wait_video = False
        users[message.chat.id].right_answers += 1
        bot.send_message(message.chat.id, f'Окей, идём дальше!')
        ask_quistion(message)
        bot.forward_message('-1001177320853', message.chat.id, message.id)
    else:
        if not users[message.chat.id].go:
            bot.send_message(message.chat.id, f'Для запуска викторины напиши /go')


@bot.message_handler(
    content_types=['audio', 'photo', 'sticker', 'video_note', 'voice', 'location', 'contact', 'new_chat_members',
                   'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
                   'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id',
                   'pinned_message'])
def return_media(message):
    if message.chat.id not in users:
        bot.send_message(message.chat.id,
                         f'Мы как-то пропустили момент со знакомством, пиши /start и я тебя запомню...')
    else:
        if not users[message.chat.id].go:
            bot.send_message(message.chat.id, f'Для запуска викторины напиши /go')
        else:
            if users[message.chat.id].wait_video:
                bot.send_message(message.chat.id, f'Не-не-не, не то, жду видео!')


@bot.message_handler(content_types=['document'])
def return_document(message):
    file_name = message.document.file_name
    file_name = file_name.split('.')
    file_name = file_name[len(file_name) - 1].upper()
    if file_name in ['MOV', 'MPEG4', 'MP4', 'AVI', 'WMV', 'MPEGPS', 'FLV', '3GP']:
        return_video(message)
    else:
        return_media(message)


bot.polling()
