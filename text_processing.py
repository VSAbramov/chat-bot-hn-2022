import re
import numpy

TOO_SHORT = 0
WRONG = 1
RIGHT = 2 

MIN_ANS_LEN = 20

def answer_estimate(st_ans, text):
    if (len(st_ans)<MIN_ANS_LEN):
        ex_ans = "Не скупитесь на слова, расскажите, что вы знаете, подробнее."
        return (ex_ans, TOO_SHORT)
    if (estim_answer(st_ans, text)>0):
        ex_ans = "Вы меня поразили! Продолжайте заниматься в том же духе, и вы станете лучшим в своём деле!"
        return(ex_ans, RIGHT)
    else:
        ex_ans = "Мне кажется, что вам стоит лучше разобрать эту тему."
        return(ex_ans, WRONG)

def extract_words(text=''):
    # перевод в нижний регистр
    text = text.lower()

    # разделителем является любой символ, не являющийся буквой
    words_raw = re.split('[^a-zа-я]', text)

    # необходимо, чтобы можно было использовать маску
    words = numpy.array(words_raw)

    mask = list(map(lambda x: len(x)>3, words_raw))
    words = list(words[mask])
    return words

# return dict { "unique word" : mentions number }
def construct_dict(words):
    word_cnt = {}
    for word in words:
        word_cnt.setdefault(word, 0)
        word_cnt[word]+=1
    return word_cnt

def get_keywords(words):
    # from https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
    word_cnt = construct_dict(words)
    keywords_list = list(dict(sorted(word_cnt.items(), key=lambda item: item[1], reverse= True)))
    keywords = set(keywords_list[:15])
    return keywords
    

def estim_answer(msg_text, text):
    words_set = set(extract_words(msg_text))
    keywords = get_keywords(extract_words(text))

    key_used = words_set.intersection(keywords)

    if (len(key_used)/len(keywords)>0.2):
        return 1
    else:
        return 0