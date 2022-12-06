import os  # Импортируем библиотку для работы с ОС
from ui.book_formatter import BookFormatter


def draw_ui(strings_ui: str):
    print(strings_ui)


def clear():
    clear_console = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear_console()


def print_books(books):
    print(BookFormatter.format_books(books))


def print_book(book):
    print(f'Ваша книга: {BookFormatter.format_book(book)}')


def is_pdf():
    while True:
        result = input('Хотите получить вывод в pdf? (y/n)\n')
        if result == 'y':
            return True
        elif result == 'n':
            return False

        print('Ошибка формата. Повторите ввод.')


def get_input():
    while True:
        user_input = input('Введите команду.\n')
        return user_input


def get_single_input():
    return input('Введите значение:\n')


def get_parameterized_input(text: str):
    return input(text + '\n')


def confirm_input():
    input("Нажмите Enter, чтобы продолжить...")


def get_sting():
    user_input = None
    while True:
        try:
            user_input = str(input('Введите строку число.\n'))
            return user_input
        except Exception as e:
            print(e)
