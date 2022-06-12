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
#  взаимодействуетс ботом в основном через кнопки.
###########################################################
@bot.message_handler(commands = ['start'])
def start(message):
    try:
        msg = f'Привет, {message.from_user.first_name}'
        start_screen(message, msg)
    #except:
    except BaseException as e:
        print(str(e))
        bot.send_message(message.chat.id, 'something went wrong at start')

@bot.message_handler(commands=['info'])
def info(message):
    try:
        msg = str(message)
        bot.send_message(message.chat.id, msg)
    except:
        bot.send_message(message.chat.id, 'something went wrong at info')

@bot.message_handler(commands=['bot_state'])
def bot_state(message):
    state = bt.bot_state
    bot.send_message(message.chat.id, str(state))

@bot.message_handler(commands=['lvlup'])
def lvlup(message):
    '''
    призвана моделировать внешний сигнал, о том, что пользователь 
    продвинулся в своём курсе, чтобы на это мог отреагировать его 
    аватар 
    '''
    character.lvlup()
    pic = character.give_avatar_address()
    send_picture(message, pic)
    bot.send_message(message.chat.id, 'Благодаря твоим стараниям я вырос и стал лучше!')

@bot.message_handler(commands=['check_lvl'])
def check_lvl(message):
    lvl = character.level
    bot.send_message(message.chat.id, str(lvl))

@bot.message_handler(commands=['reset'])
def reset(message):
    bt.bot_state = bt.DEFAULT_ST
    remove_buttons(message, 'Начнём диалог сначала!')

@bot.message_handler(commands=['cancel'])
def cancel(message):
    start_screen(message, 'возвращаю начальный экран')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, ''' 
    Список доступных команд для пользователя:
    /start -- начать взаимодействие,
    /help -- вывести данное сообщение,
    /reset -- сборить бот (после чего снова нужно будет вызвать /start)
    /cancel -- вернуться на начальный экран

    Команды для отладки и симуляции сигналов из вне:
    lvlup,
    check_lvl,
    info,
    bot_state    
    ''')

@bot.message_handler(regexp="^/.*")
def wrong_command(message):
    bot.send_message(message.chat.id, ''' 
    неизвестная команда, используй команду /help, чтобы просмотреть список доступных команд
    '''
    )  
#--------------------------------------------------------------------


############################################################
# обработка пользовательских команд в виде кнопок и текста
############################################################
@bot.message_handler()
def process_user_input(message):
    '''
    управление текстовыми командами, основываясь на состояниях бота.
    
    мотивация:
    Если нажатие предыдущей кнопки ожидает продолжение взаимодействия, 
    то нму надо реагировать особым образом на следующие текстовые сообщения.
    Таким образом данная функция управляет потоком поведения бота в диалоге.
    '''
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

        elif (bt.bot_state == bt.CHOOSING_EXAM_ST):
            exam_question(message)
        
        elif (bt.bot_state == bt.EXAM_ST):
            exam_grade(message)

        elif (bt.bot_state == bt.CHOOSING_EXER_ST):
            give_exercise(message)
            
        elif (bt.bot_state == bt.EXER_ST):
            give_answer(message)

    except BaseException as e:
        print(str(e))
        start_screen(message, 'произошла ошибка, возвращаюсь на начальный экран')


def proc_cmd_oper_st(message):
    '''
    обработка кнопок 'верхнего уровня' (OPERATIONAL_ST)
    '''
    cmd = message.text
    if cmd == bt.USER_COMMANDS['avatar']:
        show_avatar(message)
    elif cmd == bt.USER_COMMANDS['exam']:
        ask_for_course(message)
        bt.bot_state = bt.CHOOSING_EXAM_ST
    elif cmd == bt.USER_COMMANDS['fun']:
        char_fun(message)
    elif cmd == bt.USER_COMMANDS['exercise']:
        ask_for_course(message)
        bt.bot_state = bt.CHOOSING_EXER_ST
    else:
        msg = 'пожалуйста, выберите кнопку, или используйте команду /reset'
        bot.send_message(message.chat.id, msg)

def exam_grade(message):
    msg_text = message.text
    text = character.load_course_text()
    text, grade = text_processing.answer_estimate(msg_text, text)    
    bot.send_message(message.chat.id, text)
    if (grade == text_processing.RIGHT):
        pic = character.give_avatar_address()
        send_picture(message, pic)

    # если ответ не слишком короткий, не ждать повторного ответа
    if not grade==text_processing.TOO_SHORT:
        text = 'Что хочешь делать дальше?'
        start_screen(message, text)

def exam_question(message):
    course = message.text
    character.chosen_course = course
    remove_buttons(message, 'расскажите, что вы знаете о курсе "' + course + "'" )
    bt.bot_state = bt.EXAM_ST

def char_fun(message):
    pic, caption = character.get_fun_picture()
    send_picture(message, pic)
    bot.send_message(message.chat.id, caption)

def ask_for_course(message):
    courses = character.get_courses()
    buttons = []
    for course in courses:
        buttons.append(types.KeyboardButton(course))
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for button in buttons:
        markup.add(button)

    bot.send_message(message.chat.id, 'Выберите курс', reply_markup=markup)

def give_exercise(message):
    bt.bot_state = bt.EXER_ST
    character.chosen_course = message.text
    text = character.get_exercise(message)
    #bot.send_message(message.chat.id, text)
    remove_buttons(message, text)

def give_answer(message):
    bt.bot_state = bt.OPERATIONAL_ST
    ans = character.give_ex_answer(message.text)
    start_screen(message, ans)

def show_avatar(message):
    pic = character.give_avatar_address()
    send_picture(message, pic)
#-------------------------------------------------------------------------



############
# утилиты
############
def send_picture(message, pic):
    try:
        with open(pic, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except:
        with open('./pictures/ex.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)


def remove_buttons(message, text):
    delete_buttons = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, text, reply_markup=delete_buttons)


def start_screen(message, text):
    '''
    Представить пользователю начальный экран, от куда начинается 
    взаимодействие. Тут создаются основные кнопки.

    Каждой кнопке изменяющее поведение бота,  соответсвует свой 
    статус в bot_state.py 
    '''
    bt.bot_state = bt.OPERATIONAL_ST

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    but_1 = types.KeyboardButton(bt.USER_COMMANDS['avatar'])
    but_2 = types.KeyboardButton(bt.USER_COMMANDS['fun'])
    but_3 = types.KeyboardButton(bt.USER_COMMANDS['exam'])
    but_4 = types.KeyboardButton(bt.USER_COMMANDS['exercise'])
    markup.add(but_1, but_2)
    markup.add(but_3, but_4)

    bot.send_message(message.chat.id, text, reply_markup=markup)

bot.polling(non_stop = True) 
