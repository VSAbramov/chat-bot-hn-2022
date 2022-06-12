# общее описание чат-бота

Чат-бот создаёт дружелюбную атмосферу, поддерживая заинтересованность студента в обучении. Особенностью данного чат-бота является возможность помощи студентам в рефлексии пройденного материала: система просит учащегося пересказать информацию своими словами и автоматически её оценивает. Бот подсказывает, когда стоит повторить пройденный материал. Также для вовлечённых в процесс обучения студентов чат-бот даёт отдельные задачи, имеющие единственно правильный ответ.

В нашем боте присутствует элемент игрофикации: практикуется развитие персонажа по принципу Тамагочи. Герой (байкальская нерпа Ботик) растёт по мере прохождения каждой темы, модуля, блока заданий. В боте имеется не только элемент бейджификации (новая, улучшенная версия персонажа в ответ на достижение), но и сюжетная линия (нерпа растёт, умнеет, ставит новые цели и добивается их), помогающий поддерживать интерес к персонажу. Также в боте есть кнопка, позволяющая "узнать", чем занимается персонаж в данный момент; случайным образом показывается изображение нерпы за различными занятиями с соответствующим текстом. Набор картинок и текста задан заранее для каждого уровня. Однако для сохранения фокуса внимания текст в большинстве случаев мягко подбадривает учащегося в его прохождении курса.

Стремление создать комфортную психологическую обстановку и поддерживать заинтересованность в обучении помогает студенту в его мотивации достижения успеха для эффективного прохождения курса.

# как пользоваться ботом
Для начала работы надо передать команду /start, после чего отобразятся кнопки. В дальнейшем взаимодействие с ботом идёт через кнопки, кроме случаев, когда бот просит пользователя написать ответ на поставленную задачу. В случае возникновения проблемы есть команды /reset (сбросить всё на начальные настройки) и /cancel (перейти на начальный экран); информация о доступных командах написана в справке, вызываемой с помощью /help.

# структура программы бота 

Бот, описанный в файле main.py, отвечает за взаимодействие с пользователем, персонаж, описанный в Character.py, описывает данные пользователя. Бот обращается к персонажу, чтобы получить необходимые данные, например, имя картинки, которую надо отправить пользователю. В отдельный файл bot_state.py вынесены параметры бота. В отдельный файл text_pocessing.py вынесена функция, которая оценивает правильность ответа пользователя.

![image](https://user-images.githubusercontent.com/48627015/173253065-52e436b3-cfb2-4701-a879-1201aa2ea8b3.png)
