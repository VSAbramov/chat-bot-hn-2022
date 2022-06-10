from codecs import charmap_encode
from click import command
import telebot
import json

import ast
import pprint
from Character import Character

character = Character()

bot = telebot.TeleBot('5387710154:AAFPpNY1V_eO6IraDtnPZ8DvO3nP7bIjZj4')   


@bot.message_handler(commands = ['start'])
def start(message):
    try:
        #mess = f'Привет, {message.from_user}'
        mess = f'Привет, {message.from_user.first_name}'
        #bot.send_message(message.chat.id, 'Hello world!')
        bot.send_message(message.chat.id, mess)

        #if (not character):
        #    character = Character(message.from_user.id)
    except:
        bot.send_message(message.chat.id, "something went wrong")

@bot.message_handler(commands=['info'])
def info(message):
    try:
        msg = str(message)
        pp = pprint.PrettyPrinter(indent= 4)
        msg = pp.pformat(ast.literal_eval(msg))
        bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, "something went wrong")

@bot.message_handler(commands=['lvlup'])
def lvlup(message):
    character.lvlup(message, give_pictue)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, ''' 
    Список доступных комманд:
    start, 
    info, 
    help,
    lvlup
    ''')


@bot.message_handler(regexp="/.*")
def wrong_command(message):
    bot.send_message(message.chat.id, ''' 
    неизвестная комманда, используй комманду /help, чтобы просмотреть список доступных комманд
    '''
    )  

@bot.message_handler()
def get_user_text(message):
    text = message.text
    bot.send_message(message.chat.id, message.text)



def give_pictue(message, text=''):
    photo = open('./pictures/ex.jpg', 'rb')
    print(type(message))
    bot.send_photo(message.chat.id, photo)

bot.polling(non_stop = True) 
