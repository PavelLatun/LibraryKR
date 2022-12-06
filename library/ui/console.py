import os  # Импортируем библиотку для работы с ОС
from ui.book_formatter import BookFormatter


class ConsolePrinter:

    @staticmethod
    def draw_ui(strings_ui: str):
        print(strings_ui)

    @staticmethod
    def clear():
        clear_console = lambda: os.system('cls' if os.name == 'nt' else 'clear')
        clear_console()

    @staticmethod
    def print_books(books):
        print(BookFormatter.format_books(books))

    @staticmethod
    def print_book(book):
        print(f'Ваша книга: {BookFormatter.format_book(book)}')

    @staticmethod
    def is_pdf():
        while True:
            result = input('Хотите получить вывод в pdf? (y/n)\n')
            if result == 'y':
                return True
            elif result == 'n':
                return False

            print('Ошибка формата. Повторите ввод.')

    @staticmethod
    def get_input():
        while True:
            user_input = input('Введите команду.\n')
            return user_input

    @staticmethod
    def get_single_input():
        return input('Введите значение:\n')

    @staticmethod
    def get_parameterized_input(text: str):
        return input(text + '\n')

    @staticmethod
    def confirm_input():
        input("Нажмите Enter, чтобы продолжить...")
