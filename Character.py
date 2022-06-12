from random import randint

class Character:
    '''
    автар пользователя, отвечает за всю информацию, касающуюся пользователя.

    сохраняет прогресс, знает где лежат все необходимые материалы
    '''
    
    level = 1
    chosen_course = ''

    def __init__(self, id_from_msg=1):
        id = id_from_msg

    def lvlup(self):
        self.level += 1

    def load_course_text(self):
        file_name = self.get_course_file_name()
        with open(file_name, "r") as file:
            text = file.read()
        return text

    def give_avatar_address(self):
        '''
        передаёт расположение файла с картинкой персонажа
        '''
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
        '''
        передаёт расположение файла с текстом курса по выбранной теме
        (на практике должна быть значительно более сложной, чтобы найти 
         и передать нужный текст)
        '''
        if self.chosen_course == 'психология':
            return './courses_texts/психология.txt'
        elif self.chosen_course == 'литература':
            return './courses_texts/литература.txt'
        elif self.chosen_course == 'python':
            return './courses_texts/python.txt'
        elif self.chosen_course == 'data science':
            return './courses_texts/data science.txt'

    def get_fun_picture(self):
        try:
            filename = './pictures/fun.' + str(self.level) + '.txt'
            with open(filename, 'r') as file:
                lines = file.readlines()

            pic_num = randint(1,3)
            pic = './pictures/fun.' + str(self.level) + '.' + str(pic_num) + '.jpg'
            return pic, lines[pic_num-1]
        except:
            return './pictures/ex.jpg', 'Пингвины!'

    def get_exercise(self, message):
        ''' 
        для экономии времени и возможности демоснтрации, вопросы
        записаны прямо в коде, но предполагается, что данная функция
        должна выбирать рандмно вопрос по выбранному курсу
        '''
        if self.chosen_course == 'литература':
            return '''
...Люблю тебя, Петра творенье,
Люблю твой строгий, стройный вид,
Невы державное теченье,
Береговой ее гранит...
            
Из какой поэмы А.С.Пушкина эта цитата?           
            '''
        elif self.chosen_course == 'психология':
            return '''
побуждение к действию; психофизиологический процесс, управляющий поведением человека, задающий его направленность, организацию, активность и устойчивость; способность человека деятельно удовлетворять свои потребности.

Как одним словом назвать этот процесс?
            '''
        elif self.chosen_course == 'data science':
            return 'Какой из двух методов лучше подходит для решения задач классификации, KNN или линейная регрессия?'
            
        elif self.chosen_course == 'python':
            return 'Используя какую стандартную функцию можно выяснить количество элементов в списке?'
        return 'Пингвины!'

    def give_ex_answer(self, stud_ans):
        '''
        соответственно ответ тоже должен храниться во внешней базе
        '''
        if self.chosen_course == 'литература':
            if 'медный всадник' in stud_ans.lower():
                return 'Правильно!'
            else:
                return 'Неверно! Правильный ответ "Медный всадник"'
        elif self.chosen_course == 'психология':
            if 'мотивация' in stud_ans.lower():
                return 'Правильно!'
            else:
                return 'Неверно! Правильный ответ "Мотивация"'
        elif self.chosen_course == 'data science':
            if 'knn' in stud_ans.lower():
                return 'Правильно!'
            else:
                return 'Неверно! Правильный ответ "KNN"'
        elif self.chosen_course == 'python':
            if 'len' in stud_ans.lower():
                return 'Правильно!'
            else:
                return 'Неверно! Предполагаемый ответ "len()"'
        return "Пингвины!"