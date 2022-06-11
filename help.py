# взял из одного урока в качестве справки
import re
import numpy
from scipy import spatial

def some_func():
    #Каждая строка в файле соответствует одному предложению. 
    # Считайте их, приведите каждую к нижнему регистру с помощью 
    # строковой функции lower().  
    file_obj = open('sentences.txt', 'r')
    strs = []
    for str_from_file in file_obj:
        strs.append(str_from_file)
    file_obj.close()

    # Произведите токенизацию, то есть разбиение текстов на слова. 
    # Для этого можно воспользоваться регулярным выражением, которое 
    # считает разделителем любой символ, не являющийся буквой: 
    #    re.split('[^a-z]', t). 
    # Не забудьте удалить пустые слова после разделения.

    def split_func(a):
        return re.split('[^a-z]',a)

    # разделить строки на слова и поместить полученный список в 
    # элемент другого списка
    words_raw = list(map(split_func, strs))


    # перевести каждый элемент списка words_raw в вид numpy.array
    words = list(map(numpy.array, words_raw))

    # удаление пустых символов
    for i in range(len(words)):
        words[i]=words[i][words[i]!='']

    # Составьте список всех слов, встречающихся в предложениях. 
    # Сопоставьте каждому слову индекс от нуля до (d - 1), 
    # где d — число различных слов в предложениях. Для этого удобно 
    # воспользоваться структурой dict.

    # составить из списка списков одномерный список 
    words_arr = []
    for words_from_string in words_raw:
        words_arr.extend(words_from_string)
    # удаление пустых символов
    words_arr = numpy.array(words_arr)
    index = numpy.argwhere(words_arr=='')
    words_arr =numpy.delete(words_arr, index)

    unique_words = numpy.unique(words_arr)
    unique_words_dict = dict()
    for i in range(len(unique_words)):
        unique_words_dict[unique_words[i]]=i    

    # Создайте матрицу размера n * d, где n — число предложений. Заполните 
    # ее: элемент с индексом (i, j) в этой матрице должен быть 
    # равен количеству вхождений j-го слова в i-е предложение. У 
    # вас должна получиться матрица размера 22 * 254.  
    # i - номер предложения  
    # j - индекс слова в словаре  
    # $a_{ij}$ - количество в i-ом предложении слова с индексом j

    # создание матрицы A (которая описана в задании)
    A = numpy.zeros((len(words),len(unique_words_dict)))

    for i in range(len(words)):
        a = numpy.unique(words[i], return_counts=True)
        #print("i=", i, "| ",end = " ")
        for j in range(len(a[1])):
            i_idx = i
            j_idx = unique_words_dict[words[i][j]]
            #print(a[1][j], end = " ")
            A[i_idx, j_idx] = a[1][j]
        #print('')
        


    # Найдите косинусное расстояние от предложения в самой первой строке 
    # (In comparison to dogs, cats have not undergone...) до всех остальных 
    # с помощью функции scipy.spatial.distance.cosine. Какие номера у двух 
    # предложений, ближайших к нему по этому расстоянию (строки нумеруются 
    # с нуля)? Эти два числа и будут ответами на задание. Само предложение 
    # (In comparison to dogs, cats have not undergone... ) имеет индекс 0.

    dist = []
    for i in range(len(A)):
        dist.append(scipy.spatial.distance.cosine(A[0],A[i]))

    sorted_dist = numpy.sort(dist)

    answer = [dist.index(sorted_dist[1]),dist.index(sorted_dist[2])]
    answer