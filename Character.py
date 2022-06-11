from matplotlib.pyplot import text


class Character:
    """
    This is an avatar for interaction with user.

    It shows character state with picture. 
    It shows it's state every time when status is changing or by 
    dirrect command.
    """
    
    level = 1
    state = 0


    def __init__(self, id_from_msg=1):
        id = id_from_msg

    def show_state(self, msg, send_msg):
        text = str(self.level)
        send_msg(msg.chat.id, text)

    def lvlup(self, msg, bot_send_pic, text=''):
        self.level += 1
        #pic = './pictures/ex.jpg'
        #send_pic(msg, pic)
        self.send_pic(msg, bot_send_pic)

    def send_pic(self, msg, bot_send_pic):
        pic = './pictures/ex.jpg'
        if (self.level == 1): pic = './pictures/1.jpg'
        elif (self.level == 2): pic = './pictures/2.jpg'
        elif (self.level == 3): pic = './pictures/3.jpg'
        elif (self.level == 4): pic = './pictures/4.jpg'
        elif (self.level == 5): pic = './pictures/5.jpg'
        elif (self.level == 6): pic = './pictures/6.jpg'
        elif (self.level == 7): pic = './pictures/7.jpg'
        
        bot_send_pic(msg, pic)

    def load_course_text(self):
        with open('./courses_texts/ex_1.txt', "r") as file:
            text = file.read()
        return text

