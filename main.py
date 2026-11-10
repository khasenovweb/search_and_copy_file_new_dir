import os
import shutil
from pathlib import Path
import re

def find_and_copy_files_by_name(source_dir, target_dir, filename_to_find, exact_match=True):
    """
    Ищет файлы по названию и копирует их в целевую директорию
    
    Параметры:
    source_dir (str): Исходная директория для поиска
    target_dir (str): Целевая директория для копирования
    filename_to_find (str): Название файла для поиска
    exact_match (bool): True - точное совпадение, False - частичное совпадение
    """
    
    # Создаем целевую директорию, если она не существует
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    # Счетчик найденных файлов
    found_count = 0
    
    # Проходим по всем файлам и поддиректориям
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            # Проверяем соответствие имени файла
            if exact_match:
                match = file == filename_to_find
            else:
                # Ищем частичное совпадение (без учета регистра)
                match = filename_to_find.lower() in file.lower()
            
            if match:
                found_count += 1
                
                # Полный путь к исходному файлу
                source_path = os.path.join(root, file)
                
                # Получаем относительный путь от исходной директории
                rel_path = os.path.relpath(root, source_dir)
                
                if rel_path == '.':
                    # Если файл в корневой директории
                    prefix = ""
                else:
                    # Заменяем разделители путей на дефисы или другие символы
                    prefix = rel_path.replace(os.sep, '_') + '_'
                
                # Формируем новое имя файла с префиксом пути
                new_filename = prefix + file
                target_path = os.path.join(target_dir, new_filename)
                
                try:
                    # Копируем файл
                    shutil.copy2(source_path, target_path)
                    print(f"✓ Скопирован: {source_path} -> {target_path}")
                except Exception as e:
                    print(f"✗ Ошибка при копировании {source_path}: {e}")
    
    print(f"\nНайдено файлов: {found_count}")
    print(f"Файлы скопированы в: {target_dir}")

def find_and_copy_files_by_pattern(source_dir, target_dir, pattern):
    """
    Ищет файлы по регулярному выражению и копирует их
    
    Параметры:
    source_dir (str): Исходная директория для поиска
    target_dir (str): Целевая директория для копирования
    pattern (str): Регулярное выражение для поиска файлов
    """
    
    # Создаем целевую директорию, если она не существует
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    
    # Счетчик найденных файлов
    found_count = 0
    regex = re.compile(pattern)
    
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if regex.search(file):
                found_count += 1
                
                source_path = os.path.join(root, file)
                rel_path = os.path.relpath(root, source_dir)
                
                if rel_path == '.':
                    prefix = ""
                else:
                    prefix = rel_path.replace(os.sep, '_') + '_'
                
                new_filename = prefix + file
                target_path = os.path.join(target_dir, new_filename)
                
                try:
                    shutil.copy2(source_path, target_path)
                    print(f"✓ Скопирован: {source_path} -> {target_path}")
                except Exception as e:
                    print(f"✗ Ошибка при копировании {source_path}: {e}")
    
    print(f"\nНайдено файлов: {found_count}")
    print(f"Файлы скопированы в: {target_dir}")

def main():
    """
    Пример использования функций
    """
    # Настройки поиска
    SOURCE_DIRECTORY = "/Users/khasenovweb/Desktop/Яндекс карты база/россия"
    TARGET_DIRECTORY = "/Users/khasenovweb/Desktop/маркетинговые агенства России"
    FILENAME_TO_FIND = "Интернет-маркетинг.xlsx"  # Название файла для поиска
    
    # Вариант 1: Точный поиск по имени файла
    print("=== Поиск по точному имени ===")
    find_and_copy_files_by_name(
        source_dir=SOURCE_DIRECTORY,
        target_dir=TARGET_DIRECTORY,
        filename_to_find=FILENAME_TO_FIND,
        exact_match=True
    )
    
    # # Вариант 2: Поиск по части имени (например, все .txt файлы)
    # print("\n=== Поиск по части имени (.txt файлы) ===")
    # find_and_copy_files_by_name(
    #     source_dir=SOURCE_DIRECTORY,
    #     target_dir=TARGET_DIRECTORY,
    #     filename_to_find=".txt",
    #     exact_match=False
    # )
    
    # # Вариант 3: Поиск по регулярному выражению
    # print("\n=== Поиск по регулярному выражению ===")
    # # Найти все файлы, начинающиеся на "report" и заканчивающиеся на .csv или .xlsx
    # PATTERN = r'^report.*\.(csv|xlsx)$'
    # find_and_copy_files_by_pattern(
    #     source_dir=SOURCE_DIRECTORY,
    #     target_dir=TARGET_DIRECTORY,
    #     pattern=PATTERN
    # )

def interactive_mode():
    """
    Интерактивный режим работы
    """
    print("=== Поиск и копирование файлов с сохранением структуры в имени ===")
    
    # Запрашиваем пути у пользователя
    source_dir = input("Введите путь к исходной директории: ").strip()
    if not os.path.exists(source_dir):
        print("Ошибка: Исходная директория не существует!")
        return
    
    target_dir = input("Введите путь к целевой директории: ").strip()
    
    print("\nВыберите тип поиска:")
    print("1 - Точное совпадение имени файла")
    print("2 - Частичное совпадение (поиск по подстроке)")
    print("3 - Поиск по регулярному выражению")
    
    choice = input("Ваш выбор (1-3): ").strip()
    
    if choice == "1":
        filename = input("Введите точное имя файла для поиска: ").strip()
        find_and_copy_files_by_name(source_dir, target_dir, filename, exact_match=True)
    
    elif choice == "2":
        substring = input("Введите подстроку для поиска в именах файлов: ").strip()
        find_and_copy_files_by_name(source_dir, target_dir, substring, exact_match=False)
    
    elif choice == "3":
        pattern = input("Введите регулярное выражение: ").strip()
        find_and_copy_files_by_pattern(source_dir, target_dir, pattern)
    
    else:
        print("Неверный выбор!")

if __name__ == "__main__":
    # Запуск интерактивного режима
    # interactive_mode()
    
    # Или раскомментируйте для использования с заданными параметрами:
    main()