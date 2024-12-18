import csv
import pickle

# Функция сохранения таблицы в Pickle файл
def save_table_to_pickle(dict_table, file_path):
    """
    Сохраняет словарь в Pickle файл.
    dict_table: словарь, где ключи - заголовки колонок, значения - данные
    file_path: путь к файлу для сохранения
    """
    try:
        with open(file_path, mode='wb') as file: #mode='wb':
            # w: Режим записи (write) — файл создаётся или перезаписывается.
            # b: Бинарный режим — используется для работы с файлами Pickle.
            pickle.dump(dict_table, file)
            # pickle.dump(): Функция из модуля pickle, которая сериализует (кодирует) Python-объект и записывает его в файл
    except IOError:
        return 'Ошибка сохранения файла'

# Функция сохранения в текстовый файл
def save_table_to_text(dict_table, file_path):
    """
    Сохраняет таблицу в текстовый файл.
    file_path: путь к файлу
    """
    try:
        with open(file_path, mode='w', encoding='utf-8') as file: # as file: Создаёт переменную file для взаимодействия с открытым файлом.
            file.write(' '.join(dict_table.keys()) + '\n')
            # dict_table.keys(): Получает список ключей из словаря (названия колонок).
            # ' '.join(...): Объединяет элементы списка в строку, используя пробел ' ' в качестве разделителя. Результат: 'Name Age'.
            # file.write(): Записывает строку в файл.
            for row in zip(*dict_table.values()):
                # Функция zip() объединяет элементы из нескольких списков по их индексам.
                # * распаковывает списки из dict_table.values() в аргументы функции zip.
                file.write(' '.join(map(str, row)) + '\n') #
                # Объединяет элементы строки row в одну строку с пробелами между значениями.
                # row = ('Alice', 25) -> ' '.join(map(str, row)) = 'Alice 25'
    except IOError:
        return 'Ошибка сохранения файла'

# Получение типов столбцов
def get_column_types(dict_table, by_number=True):
    """
    Получение словаря вида столбец:тип_значений.
    by_number: если True, используется индекс столбца, иначе имя.
    """
    try:
        result = {}  # Создаём пустой словарь для хранения типов данных столбцов.

        for idx, (key, values) in enumerate(dict_table.items()):
            # Проходим по всем столбцам таблицы:
            # - idx: индекс столбца.
            # - key: имя столбца.
            # - values: список значений в столбце.

            column_type = type(values[0]) if values else str
            # Определяем тип первого элемента столбца, если столбец не пустой.
            # Если столбец пустой (values=[]), используем тип `str` по умолчанию.

            result[idx if by_number else key] = column_type
            # В словарь `result` сохраняем тип столбца:
            # - Ключ: индекс столбца (если `by_number=True`) или имя столбца.
            # - Значение: тип данных столбца.

        return result  # Возвращаем словарь с типами данных для всех столбцов.

    except Exception as e:
        return f'Ошибка: {e}'  # Возвращаем сообщение об ошибке при возникновении исключений.

# Установка типов столбцов
def set_column_types(dict_table, types_dict, by_number=True):
    """
    Установка типов значений для столбцов.
    types_dict: словарь столбец:тип_значений.
    by_number: если True, используется индекс столбца, иначе имя.
    """
    try:
        keys = list(dict_table.keys())  # Преобразуем ключи словаря (имена столбцов) в список.

        for col, col_type in types_dict.items():
            # Проходим по всем элементам словаря types_dict:
            # - col: индекс или имя столбца.
            # - col_type: функция преобразования типа (например, int, float, str).

            column_key = keys[col] if by_number else col
            # Определяем ключ столбца:
            # - Если `by_number=True`, используем индекс для получения ключа из `keys`.
            # - Если `by_number=False`, ключ передан напрямую.

            dict_table[column_key] = list(map(col_type, dict_table[column_key]))
            # Преобразуем значения столбца в указанный тип с помощью `map(col_type, ...)`:
            # - col_type применяется к каждому элементу столбца.
            # - Результат преобразуется в список и заменяет текущий столбец.

    except Exception as e:
        return f'Ошибка: {e}'  # Возвращаем сообщение об ошибке, если что-то пошло не так.

# Получение строк по номеру
def get_rows_by_number(dict_table, start, stop=None, copy_table=False):
    """
    Получение строк по номеру (диапазону).
    start: начальный индекс.
    stop: конечный индекс.
    copy_table: если True, возвращает копию таблицы.
    """
    try:
        stop = stop if stop is not None else start + 1
        # Если аргумент `stop` не передан, извлекаем одну строку:
        # stop = start + 1 делает диапазон [start:stop] равным одной строке.

        result = {key: value[start:stop] for key, value in dict_table.items()}
        # Для каждого столбца в таблице (key: столбец, value: список значений):
        # - Извлекаем строки с `start` по `stop` (не включая stop) с помощью среза `value[start:stop]`.
        # - Формируем новый словарь, где ключи остаются прежними, а значения — обрезанные списки.

        return result.copy() if copy_table else result
        # Если `copy_table=True`, возвращаем копию словаря.
        # Иначе возвращаем новый словарь с обрезанными значениями.

    except Exception as e:
        return f'Ошибка: {e}'  # Возвращаем сообщение об ошибке при возникновении исключений.

# Получение строк по значению индекса
def get_rows_by_index(dict_table, *indices, copy_table=False):
    """
    Получение строк по значениям индекса из первого столбца.
    indices: значения индексов.
    copy_table: если True, возвращает копию таблицы.
    """
    try:
        first_column = list(dict_table.values())[0]
        # Извлекаем первый столбец таблицы (значения первого ключа словаря).

        selected_indices = [first_column.index(i) for i in indices]
        # Проходим по значениям `indices` и ищем их индексы в первом столбце:
        # - `first_column.index(i)` возвращает индекс первого вхождения значения `i`.

        result = {key: [value[i] for i in selected_indices] for key, value in dict_table.items()}
        # Формируем новый словарь:
        # - Для каждого столбца (key: имя столбца, value: значения).
        # - Извлекаем значения с индексами, полученными выше (`selected_indices`).

        return result.copy() if copy_table else result
        # Если `copy_table=True`, возвращаем копию результата.
        # Иначе возвращаем новый словарь с извлечёнными значениями.

    except ValueError:
        return 'Ошибка: значение не найдено в первом столбце'
        # Возвращаем сообщение об ошибке, если значение не найдено в первом столбце.
    except Exception as e:
        return f'Ошибка: {e}'  # Обрабатываем другие возможные ошибки.

# Получение значений столбца
def get_values(dict_table, column=0):
    """
    Получение значений столбца.
    column: индекс или имя столбца.
    """
    try:
        keys = list(dict_table.keys())
        # Получаем список ключей (имен столбцов) из словаря.

        column_key = keys[column] if isinstance(column, int) else column
        # Определяем ключ столбца:
        # - Если column — число, используем индекс для получения имени столбца из keys.
        # - Если column — строка, используем его как имя столбца напрямую.

        return dict_table[column_key]
        # Возвращаем список значений для указанного столбца.

    except KeyError:
        return 'Ошибка: неверное имя столбца'
        # Возвращаем ошибку, если передано неверное имя столбца.
    except IndexError:
        return 'Ошибка: неверный индекс столбца'
        # Возвращаем ошибку, если индекс столбца выходит за пределы списка.

# Установка значений столбца
def set_values(dict_table, values, column=0):
    """
    Установка значений столбца.
    values: список значений.
    column: индекс или имя столбца.
    """
    try:
        keys = list(dict_table.keys())
        # Преобразуем ключи словаря (имена столбцов) в список, чтобы обращаться по индексу.

        column_key = keys[column] if isinstance(column, int) else column
        # Определяем ключ столбца:
        # - Если column — число, используем индекс.
        # - Если column — строка, считаем его именем столбца.

        if len(values) != len(dict_table[column_key]):
            # Проверяем, совпадает ли длина нового списка значений с длиной текущего столбца.
            raise ValueError('Длина значений не совпадает с длиной столбца')

        dict_table[column_key] = values
        # Обновляем значения указанного столбца на переданный список `values`.

    except Exception as e:
        return f'Ошибка: {e}'
        # Возвращаем сообщение об ошибке, если что-то пошло не так.

# Получение одного значения из столбца для одной строки
def get_value(dict_table, column=0):
    """
    Получение одного значения из столбца для таблицы с одной строкой.
    column: индекс или имя столбца.
    """
    try:
        keys = list(dict_table.keys())
        # Преобразуем ключи словаря (имена столбцов) в список, чтобы обращаться по индексу.

        column_key = keys[column] if isinstance(column, int) else column
        # Определяем ключ столбца:
        # - Если column — число, используем индекс.
        # - Если column — строка, считаем его именем столбца.

        if len(dict_table[column_key]) != 1:
            # Проверяем, что таблица содержит ровно одну строку.
            raise ValueError('Таблица содержит более одной строки')

        return dict_table[column_key][0]
        # Возвращаем первое значение из указанного столбца.

    except Exception as e:
        return f'Ошибка: {e}'
        # Возвращаем сообщение об ошибке, если что-то пошло не так.

# Установка одного значения в столбце для одной строки
def set_value(dict_table, value, column=0):
    """
    Установка одного значения в столбце для таблицы с одной строкой.
    value: новое значение.
    column: индекс или имя столбца.
    """
    try:
        keys = list(dict_table.keys())
        # Преобразуем ключи словаря (имена столбцов) в список, чтобы обращаться по индексу.

        column_key = keys[column] if isinstance(column, int) else column
        # Определяем ключ столбца:
        # - Если column — число, используем индекс.
        # - Если column — строка, считаем его именем столбца.

        if len(dict_table[column_key]) != 1:
            # Проверяем, что таблица содержит ровно одну строку.
            raise ValueError('Таблица содержит более одной строки')

        dict_table[column_key][0] = value
        # Устанавливаем новое значение в указанном столбце для первой строки.

    except Exception as e:
        return f'Ошибка: {e}'
        # Возвращаем сообщение об ошибке, если что-то пошло не так.

# Вывод таблицы на печать
def print_table(dict_table):
    """
    Выводит таблицу на печать в виде строк и столбцов.
    """
    try:
        print(' '.join(dict_table.keys()))
        # Печатаем заголовки столбцов.
        for row in zip(*dict_table.values()):
            # Используем zip для объединения значений по строкам.
            print(' '.join(map(str, row)))
            # Печатаем строку значений.
    except Exception as e:
        print(f'Ошибка при выводе таблицы: {e}')