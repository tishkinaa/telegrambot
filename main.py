import telebot

token = '1576012965:AAGdavZE7eLE_JlMgL9b9e0bCSh77hlZYDM'

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])

def start_message(message):
    bot.send_message(message.chat.id, f'пРиВЕт {message.from_user.first_name}')

bot.polling()