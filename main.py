from file1 import load_table, save_table
from file2 import get_column_types, set_column_types, save_table_to_pickle, save_table_to_text, get_value, set_value, get_rows_by_number, get_rows_by_index, get_values, set_values, print_table

# Пример использования функций
def main():
    data = {
        "Name": ["Dava", "Dzhal", "Dzhirgal"],
        "Age": [30, 25, 18],
        "City": ["Moskovskiy", "Domodedovo", "Moskva"]
    }
    save_table(data)
    table = load_table('File_1.csv', 'csv')
    print("Загруженная таблица:")
    print_table(table)

    save_table_to_text(data, 'File_1.txt')
    save_table_to_pickle(data, 'File_1.pkl')

    print("\nПолучение одного значения из столбца Name:")
    print(get_value(table, "Name"))

    print("\nУстановка одного значения в столбце Age:")
    set_value(table, 30, "Age")
    print_table(table)

    print("\nПолучение строк по номеру (0-2):")
    print_table(get_rows_by_number(table, 0, 2))

    print("\nПолучение строк по значениям индекса (Alice, Charlie):")
    print_table(get_rows_by_index(table, "Alice", "Charlie"))

    print("\nПолучение значений из столбца Age:")
    print(get_values(table, "Age"))

    print("\nУстановка значений в столбец City:")
    set_values(table, ["Boston", "San Francisco", "Seattle"], "City")
    print_table(table)

    print("\nТипы столбцов:")
    print(get_column_types(table))

    print("\nИзменение типа столбца 'Age' на строковый:")
    set_column_types(table, {1: str}, by_number=True)
    print("Таблица после изменения типа столбца:")
    print_table(table)

if __name__ == "__main__":
    main()