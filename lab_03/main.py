#импорты
import pathlib
from data_structures import Stack, Queue, LinkedList
#основные функции



#вспомогательные функции


#main


#начало программы
try:
    input_path = pathlib.Path(__file__).with_name('issues.txt')
    with input_path.open(encoding='utf-8') as input_file:
        notsort = [el.strip().split(';') for el in input_file]
except FileNotFoundError:
    print('Ошибка: файл issues.txt не найден рядом с программой.')
    raise SystemExit(1)
