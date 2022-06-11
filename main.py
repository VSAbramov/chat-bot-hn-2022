from codecs import charmap_encode
from click import command
import telebot

#import ast
#import pprint
from Character import Character
import text_processing

DEFAULT_ST = 0
EXAM_ST = 1

bot_state = DEFAULT_ST

# временное решение, на каждого пользователя должен создаваться свой объект
character = Character()

bot = telebot.TeleBot('5387710154:AAFPpNY1V_eO6IraDtnPZ8DvO3nP7bIjZj4')   

# --- обработка комманд (начинаются с '/') ----
@bot.message_handler(commands = ['start'])
def start(message):
    try:
        mess = f'Привет, {message.from_user.first_name}'
        bot.send_message(message.chat.id, mess)
    except:
        bot.send_message(message.chat.id, "something went wrong at start")

@bot.message_handler(commands=['info'])
def info(message):
    try:
        msg = str(message)
        bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, "something went wrong at info")

@bot.message_handler(commands=['avatar'])
def lvlup(message):
    pic = character.give_avatar_address()
    send_picture(message, pic)


@bot.message_handler(commands=['lvlup'])
def lvlup(message):
    #character.lvlup(message, give_pictue)
    character.lvlup()
    pic = character.give_avatar_address()
    send_picture(message, pic)
    bot.send_message(message.chat.id, "Благодаря твоим стараниям я вырос и стал лучше!")

@bot.message_handler(commands=['check_lvl'])
def check_lvl(message):
    lvl = character.level
    bot.send_message(message.chat.id, str(lvl))

@bot.message_handler(commands=['exam'])
def exam(message):
    global bot_state
    bot_state = EXAM_ST
    bot.send_message(message.chat.id, "расскажите, что вы знаете о проблеме")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, ''' 
    Список доступных комманд:
    start, 
    info, 
    help,
    lvlup,
    avatar,
    check_lvl,
    exam
    ''')


@bot.message_handler(regexp="/.*")
def wrong_command(message):
    bot.send_message(message.chat.id, ''' 
    неизвестная комманда, используй комманду /help, чтобы просмотреть список доступных комманд
    '''
    )  
#--------------------------------------------------------------------


# обработка обычного текста
@bot.message_handler()
def get_user_text(message):
    global bot_state
    try:
        if (bot_state == DEFAULT_ST):
            text = "Я совсем недавно родился и пока понимаю только некоторые команды. Напиши /help, чтобы увидеть список всех команд."
            bot.send_message(message.chat.id, text)
            
        if (bot_state == EXAM_ST):
            msg_text = message.text
            text = character.load_course_text()
            text, grade = text_processing.answer_estimate(msg_text, text)    
            bot.send_message(message.chat.id, text)
            if (grade == text_processing.RIGHT):
                pic = character.give_avatar_address()
                send_picture(message, pic)

            if not grade==text_processing.TOO_SHORT:
                bot_state = DEFAULT_ST
        
    except BaseException as e:
        print(str(e))
        bot_state = DEFAULT_ST
        bot.send_message(message.chat.id, "something went wrong at get_user_text")



def send_picture(message, pic, text=''):
    with open(pic, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)




bot.polling(non_stop = True) 
