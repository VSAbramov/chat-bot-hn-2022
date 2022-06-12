import text_processing

class Character:
    """
    This is an avatar for interaction with user.

    It shows character state with picture. 
    It shows it's state every time when status is changing or by 
    dirrect command.
    """
    
    level = 1
    chosen_course = ''

    def __init__(self, id_from_msg=1):
        id = id_from_msg

    def lvlup(self):
        self.level += 1

    def load_course_text(self):
        file_name = self.get_course_file_name()
        #with open('./courses_texts/ex_1.txt', "r") as file:
        with open(file_name, "r") as file:
            text = file.read()
        return text

    def give_avatar_address(self):
        pic = './pictures/ex.jpg'
        if (self.level == 1): pic = './pictures/1.jpg'
        elif (self.level == 2): pic = './pictures/2.jpg'
        elif (self.level == 3): pic = './pictures/3.jpg'
        elif (self.level == 4): pic = './pictures/4.jpg'
        elif (self.level == 5): pic = './pictures/5.jpg'
        elif (self.level == 6): pic = './pictures/6.jpg'
        elif (self.level == 7): pic = './pictures/7.jpg'

        return pic

    def get_courses(self):
        return ['психология', 'литература', 'python', 'data science']

    def get_course_file_name(self):
        if self.chosen_course == 'психология':
            return './courses_texts/психология.txt'
        elif self.chosen_course == 'литература':
            return './courses_texts/литература.txt'
        elif self.chosen_course == 'python':
            return './courses_texts/python.txt'
        elif self.chosen_course == 'data science':
            return './courses_texts/data science.txt'
