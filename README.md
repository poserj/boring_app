# boring_app
Приложение использует стороннее API для рекомендации времяпрепровождения.  
Пользователь настраивает 4 входных параметра. Однако API не позволяет одновременно использвать все параметры в get-запросе. По этой причине программа делает n*4 сетевых запроса с использованием одиночных параметров, которые ввел пользователь.  
Из полученного массива данных методом ratio класса SequenceMatcher из библиотеки difflib
программа выбирает 10 наиболее подходящих и выводит в консоль.

CPU-bound задачи: вычисление схожих записей в list. \
IO-bound задачи: ввод данных пользователя, сетевые запросы к API и вывод данных на экран.  
# Схема работы приложения:
![IMG_6991](https://github.com/poserj/boring_app/assets/122611131/051daaa7-abc7-49ca-b51d-1619e7eacd86)
