# файл, хранящиц состояние бота и командя для пользователя

DEFAULT_ST = 0
EXAM_ST = 1
TEST_ST = 2
OPERATIONAL_ST = 3
CHOOSING_EXAM_ST = 4
CHOOSING_EXER_ST = 5
EXER_ST = 6


bot_state = DEFAULT_ST

USER_COMMANDS = {'avatar': 'покажись', 'exam': 'хочу проверить знания!',
                 'fun': 'чем занимаешься?', 'exercise' : 'дай задачку!'}