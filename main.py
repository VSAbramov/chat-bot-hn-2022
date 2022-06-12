from sqlalchemy import null
import telebot
from telebot import types

from Character import Character
import text_processing
import bot_state as bt

# временное решение, на каждого пользователя должен создаваться свой объект
character = Character()

bot = telebot.TeleBot('5387710154:AAFPpNY1V_eO6IraDtnPZ8DvO3nP7bIjZj4')   

###########################################################
#  обработка команд (начинаются с '/').
#  данные команды используются для отладки и для симуляции 
#  внешних сигналов. Предполагается, что пользователь 
#  взаимодействуетс ботом только через кнопки.
###########################################################
@bot.message_handler(commands = ['start'])
def start(message):
    try:
        msg = f'Привет, {message.from_user.first_name}'
        start_screen(message, msg)
    except:
        bot.send_message(message.chat.id, 'something went wrong at start')

@bot.message_handler(commands=['info'])
def info(message):
    try:
        msg = str(message)
        bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, 'something went wrong at info')

@bot.message_handler(commands=['avatar'])
def avatar(message):
    pic = character.give_avatar_address()
    send_picture(message, pic)


@bot.message_handler(commands=['lvlup'])
def lvlup(message):
    character.lvlup()
    pic = character.give_avatar_address()
    send_picture(message, pic)
    bot.send_message(message.chat.id, 'Благодаря твоим стараниям я вырос и стал лучше!')

@bot.message_handler(commands=['check_lvl'])
def check_lvl(message):
    lvl = character.level
    bot.send_message(message.chat.id, str(lvl))

@bot.message_handler(commands=['exam'])
def exam(message):
    bt.bot_state = bt.EXAM_ST
    remove_buttons(message, 'расскажите, что вы знаете о проблеме')

@bot.message_handler(commands=['reset'])
def reset(message):
    bt.bot_state = bt.DEFAULT_ST
    remove_buttons(message, 'Начнём диалог сначала!')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, ''' 
    Список доступных команд:
    start, 
    help,
    lvlup,
    avatar,
    check_lvl,
    exam,
    reset,
    info
    ''')


@bot.message_handler(regexp="/.*")
def wrong_command(message):
    bot.send_message(message.chat.id, ''' 
    неизвестная команда, используй команду /help, чтобы просмотреть список доступных команд
    '''
    )  
#--------------------------------------------------------------------


############################################################
# обработка пользовательских комманд в виде кнопок и текста
############################################################
@bot.message_handler()
def process_user_input(message):
    try:
        if message.text == '':
            # после команд почему-то он отправляет пустые сообщения, 
            # пока не разберусь почему, будет этот костыль
            pass
        elif (bt.bot_state == bt.DEFAULT_ST):
            text = 'Я совсем недавно родился и пока понимаю только некоторые команды. Напиши /help, чтобы увидеть список всех команд.'
            bot.send_message(message.chat.id, text)

        elif (bt.bot_state == bt.OPERATIONAL_ST):
            proc_cmd_oper_st(message)

        elif (bt.bot_state == bt.EXAM_ST):
            proc_cmd_exam_st(message)
            
    except BaseException as e:
        print(str(e))
        bt.bot_state = bt.DEFAULT_ST
        bot.send_message(message.chat.id, 'something went wrong at get_user_text')

def proc_cmd_oper_st(message):
    cmd = message.text
    if cmd == bt.USER_COMMANDS['avatar']:
        avatar(message)
    elif cmd == bt.USER_COMMANDS['exam']:
        exam(message)
    else:
        msg = 'пожалуйста, выберите кнопку, или используйте команду /reset'
        bot.send_message(message.chat.id, msg)

def proc_cmd_exam_st(message):
    msg_text = message.text
    text = character.load_course_text()
    text, grade = text_processing.answer_estimate(msg_text, text)    
    bot.send_message(message.chat.id, text)
    if (grade == text_processing.RIGHT):
        pic = character.give_avatar_address()
        send_picture(message, pic)

    if not grade==text_processing.TOO_SHORT:
        text = 'Что хочешь делать дальше?'
        start_screen(message, text)
#-------------------------------------------------------------------------



############
# утилиты
############
def send_picture(message, pic, text=''):
    with open(pic, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


def remove_buttons(message, text):
    delete_buttons = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text, reply_markup=delete_buttons)
    #bot.send_message(message.chat.id, text, reply_markup=null)


def start_screen(message, text):
        bt.bot_state = bt.OPERATIONAL_ST

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        but_1 = types.KeyboardButton(bt.USER_COMMANDS['avatar'])
        but_2 = types.KeyboardButton(bt.USER_COMMANDS['exam'])
        markup.add(but_1, but_2)

        bot.send_message(message.chat.id, text, reply_markup=markup)

bot.polling(non_stop = True) 
