import sqlite3 as sl

class Character:
    """
    This is an avatar for interaction with user.

    It shows character state with picture. 
    It shows it's state every time when status is changing and by 
    dirrect command.
    """

    def __init__(self, id_from_msg=1):
        level = 0 
        id = id_from_msg

    def show_state(self, msg = ''):
        print("hello")

    def lvlup(self, msg, send_pic, text=''):
        #level += 1
        send_pic(msg)

