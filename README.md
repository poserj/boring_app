# boring_app
Приложение использует стороннее API для рекомендации время препровождения.  
Пользователь настраивает 4 входных параметра. Однако API не позволяет одновременно использвать в get-запросе все параметры. По этой причине программа делает n*4 сетевых запроса с использованием одиночных параметров, которые ввел пользователь.  
Из полученного массива данных методом ratio класса SequenceMatcher из библиотеки difflib
программа выбирает 10 наиболее подходящих и выводи в консоль.

CPU-bound задачи: вычисление схожих записей в list. \
IO-bound задачи: ввод данных пользователя, сетевые запросы к API и вывод данных на экран.  
