import csv
import pickle

# Функция загрузки таблицы из файла (csv, txt, pickle)
def load_table(name_table='File_1_1.csv', mode=input('Введите один из трёх форматов(csv/txt/pickle): ')):
    """
    Функция загружает данные из файла и преобразует их в словарь.
    name_table: имя файла
    mode: формат файла (csv, txt, pickle)
    """
    dict_table = {}
    if mode == 'csv':
        try:
            with open(name_table, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';') # Создаем объект для построчного чтения CSV
                header = next(reader) # Читаем первую строку, как заголовок
                data = [row for row in reader] # Эта строка генерирует список, который создает список всех строк из файла
                for col_index, col_name in enumerate(header): # Цикл, который проходит по заголовкам(header) и их индексам(col_index)
                    dict_table[col_name] = [row[col_index] for row in data]
                    # Генератор списка, который извлекает данные из каждого ряда (row) для текущего столбца (col_index)
        except IOError:
            return 'Нет доступа к файлу'
        except UnicodeDecodeError:
            return 'Файл повреждён'
    elif mode == 'txt':
        try:
            with open(name_table, mode='r', encoding='utf-8') as file: # Открытие файла
                header = file.readline().strip().split() # file.readline(): Читает первую строку файла.
                                     #.strip(): Удаляет лишние пробелы и символы переноса строки (\n) с концов строки.
                                     #.split(): Разбивает строку на отдельные слова (или значения), используя пробел как разделитель.
                data = [line.strip().split() for line in file]
                # Это генератор списка, который обрабатывает каждую строку файла (кроме уже прочитанной первой строки)
                for col_index, col_name in enumerate(header):
                    dict_table[col_name] = [row[col_index] for row in data]
                    # Генератор списка, который извлекает данные из каждого ряда (row) для текущего столбца (col_index)
        except IOError:
            return 'Нет доступа к файлу'
        except UnicodeDecodeError:
            return 'Файл повреждён'
        # 1. with open(name_table, mode='r', encoding='utf-8') as file:
        # with: Это ключевое слово, которое открывает файл и автоматически закрывает его, когда блок кода завершается. Вам не нужно вручную писать file.close(), что удобно и безопасно.
        # open(): Функция для открытия файла.
        # name_table: Имя файла, который открывается.
        # mode='r': Режим открытия. 'r' означает чтение файла.
        # encoding='utf-8': Указывает, что файл использует кодировку UTF-8 (стандартная кодировка для текстов).
        # as file: Создаёт объект file, через который вы взаимодействуете с файлом.
    elif mode == 'pickle':
        try:
            with open(name_table, mode='rb') as file:
            # b: Указывает, что файл бинарный (не текстовый). Pickle файлы хранят данные в бинарном формате, поэтому их нельзя открыть в текстовом режиме.
                dict_table = pickle.load(file) # pickle.load() восстанавливает объект в его исходной форме.
        except IOError:
            return 'Нет доступа к файлу'
        except UnicodeDecodeError:
            return 'Файл повреждён'
    else:
        return 'Неверный формат файла'
    return dict_table

# Функция сохранения таблицы в CSV файл
def save_table(dict_table):
    """
    Сохраняет словарь в CSV файл
    dict_table: словарь, где ключи - заголовки колонок, значения - данные
    """
    try:
        with open('File_1.csv', mode='w', encoding='utf-8', newline='') as file: # Открытие файла
            # newline='': Убирает добавление лишних пустых строк в CSV-файл, mode='w': Режим записи (write). Если файл существует, он будет перезаписан
            writer = csv.writer(file, delimiter=';') # Создание объекта для записи
            writer.writerow(dict_table.keys()) # Запись заголовков(ключей)
            writer.writerows(zip(*dict_table.values())) # Запись данных; writer.writerows(): Записывает сразу несколько строк в CSV-файл
            # zip(*dict_table.values()): «Склеивает» списки поэлементно, создавая строки таблицы
    except IOError:
        return 'Ошибка сохранения файла'
