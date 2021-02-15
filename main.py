import telebot
import random
import string



letters = string.ascii_lowercase
rand_string = ''.join(random.choice(letters) for i in range(10))


token = '1576012965:AAGdavZE7eLE_JlMgL9b9e0bCSh77hlZYDM'

bot = telebot.TeleBot(token)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Правлиьный ответ', 'Неправильный ответ')

questions_list = []
def ask_quistion(message):
    if questions_list:
        bot.send_message(message.chat.id, f'{questions_list.pop()}', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, f'А, нет, не идём...')
        bot.send_message(message.chat.id, f'ПОооооОбеда, твой секретный код: {rand_string.upper()}, неговори никому!!')


@bot.message_handler(commands=['start'])
def start_message(message):
    global questions_list
    questions_list = ['Вопрос №1', 'Вопрос №2', 'Вопрос №3', 'Вопрос №4']
    bot.send_message(message.chat.id, f'пРиВЕт {message.from_user.first_name}, я начинаю игру:')
    ask_quistion(message)

@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'правлиьный ответ':
        bot.send_message(message.chat.id, 'Это Правильный ответ!!!')
        bot.send_message(message.chat.id, 'Идём дальше...')
        ask_quistion(message)

    elif message.text.lower() == 'неправильный ответ':
        bot.send_message(message.chat.id, 'Это НЕ правильный ответ')
        bot.send_message(message.chat.id, f'Это ПроВаЛ(((')

bot.polling()
