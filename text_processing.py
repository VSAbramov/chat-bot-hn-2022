MIN_ANS_LEN = 20

def answer_estimate(answer):
    if (len(answer)<MIN_ANS_LEN):
        text = "Не скупитесь на слова, расскажите что вы знаете подробнее."
        return (text, 0)
    text = "Вы меня поразили! Продолжайте заниматься в том же духе и вы станете лучшим в своём деле!"
    return(text, 1)

# should return dict { "unique word" : mentions number }
def process_text(text):
    pass


