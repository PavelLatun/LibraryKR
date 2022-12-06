from abc import ABC, abstractmethod

from peewee import DoesNotExist

from model.book import Book
from repository.book import BookRep
from ui import console as ui
from model.command import Command
from model.actions import Actions
from model.event import Event
from ui.pdf import PdfPrinter


class State(ABC):
    def __init__(self, header: str, command_list):
        self.__header = header
        self.__command_list = command_list

    def __str__(self):
        string_command_list = ''

        for command in self.__command_list:
            string_command_list += command.to_string() + '\n'

        return f'{self.__header}\n{string_command_list}'

    def to_string(self, state_manager):
        string_command_list = ''

        for command in self.__command_list:
            string_command_list += command.to_string() + '\n'

        return f'{self.__header}\n{string_command_list}'

    def handle_input(self, state_manager):
        pass


class StateWithStats(State):
    def to_string(self, state_manager):
        return super().to_string(state_manager) % state_manager.book_rep.count()


class ParameterizedState(State):
    def __init__(self, header: str, command_list):
        super().__init__(header, command_list)
        self.__book = Book()

    def handle_input(self, state_manager):
        user_input = ui.get_input()

        if user_input == Actions.SetTitle.value:
            value = ui.get_single_input()
            self.set_title(value)
            state_manager.change_state(self)
        elif user_input == Actions.SetAuthor.value:
            value = ui.get_single_input()
            self.set_author(value)
            state_manager.change_state(self)
        elif user_input == Actions.SetYear.value:
            value = ui.get_single_input()
            self.set_year(value)
            state_manager.change_state(self)
        elif user_input == Actions.Execute.value:
            self.execute(state_manager)
            state_manager.change_state(self)
        elif user_input == Actions.ClearParams.value:
            self.clear_book_with_output()
            state_manager.change_state(self)
        elif user_input == Actions.Back.value:
            self.clear_book()
            state_manager.change_state(States.Main)
        else:
            ui.draw_ui('Ошибка ввода. Повторите попытку')
            pass

    def set_title(self, title: str):
        self.__book.title = title
        self.__success_update(title)

    def set_author(self, author: str):
        self.__book.author = author
        self.__success_update(author)

    def set_year(self, year: int):
        try:
            year = int(year)
            self.__book.year = year
            self.__success_update(year)
        except ValueError:
            ui.draw_ui('Ошибка формата ввода. Введите число.')

    @staticmethod
    def __success_update(param):
        ui.draw_ui(f'Параметр %s установлен.' % param)

    def clear_book_with_output(self):
        self.clear_book()
        ui.draw_ui("Все параметры очищены.")

    def clear_book(self):
        self.__book = Book()

    def get_book(self):
        return self.__book

    @abstractmethod
    def execute(self, state_manager):
        raise NotImplementedError


class MainState(StateWithStats):
    def handle_input(self, state_manager):
        user_input = ui.get_input()
        if user_input == Actions.Exit.value:
            state_manager.change_state(States.Exit)
        elif user_input == Actions.AddBook.value:
            state_manager.change_state(States.AddBook)
        elif user_input == Actions.RemoveBook.value:
            state_manager.change_state(States.RemoveBook)
        elif user_input == Actions.EditBook.value:
            state_manager.change_state(States.EditBook)
        elif user_input == Actions.FindBook.value:
            state_manager.change_state(States.FindBook)
        elif user_input == Actions.PrintAt.value:
            state_manager.change_state(States.Print)
        elif user_input == Actions.PrintAll.value:
            state_manager.change_state(States.PrintAll)
        else:
            ui.draw_ui('Ошибка ввода. Введите команду из списка.')
            pass


class AddBookState(ParameterizedState):
    def __init__(self, header: str, command_list):
        super().__init__(header, command_list)

    def execute(self, state_manager):
        state_manager.book_rep.add(self.get_book())
        ui.draw_ui(f'Книга ({self.get_book()}) добавлена.')
        self.clear_book()


class FindBookState(ParameterizedState):
    def __init__(self, header: str, command_list):
        super().__init__(header, command_list)

    def execute(self, state_manager):
        books = state_manager.book_rep.find(self.get_book())
        if books:
            ui.draw_ui('Результат поиска:')
            ui.print_books(books)
        else:
            ui.draw_ui('По вашим параметрам книги не найдены. Попробуйте еще раз.')
        self.clear_book()


class RemoveBookState(State):
    def handle_input(self, state_manager):
        user_input = ui.get_input()

        if user_input == Actions.Back.value:
            state_manager.change_state(States.Main)
        else:
            try:
                state_manager.book_rep.remove_at(user_input)
                ui.draw_ui('Книга успешно удалена')
                state_manager.change_state(States.Main)
            except ValueError:
                ui.draw_ui('Ошибка формата ввода. Введите число.')
            except DoesNotExist:
                ui.draw_ui('Не удалось удалить книгу. Книга с данным id не существует.')


class EditBookState(ParameterizedState):
    def execute(self, state_manager):
        book_id = ui.get_parameterized_input("Введите id книги для редактирования:")
        try:
            state_manager.book_rep.update_at(int(book_id), self.get_book())
            ui.draw_ui(f'Книга с id = {book_id} отредактирована.\n'
                       f'Новое состояние книги = ({state_manager.book_rep.get_at(book_id)})')
            self.clear_book()
        except ValueError:
            ui.draw_ui('Ошибка формата ввода. Введите число.')
        except DoesNotExist:
            book = self.get_book()
            ui.draw_ui('Не удалось удалить книгу. Книга с id не существует. Попробуйте ввести другой id.\n'
                       f'Текушие параметры: title = {book.title}, year = {book.year}, author = {book.author}.')


class PrintState(State):
    def handle_input(self, state_manager):
        user_input = ui.get_input()

        try:
            book = state_manager.book_rep.get_at(int(user_input))
            if ui.is_pdf():
                file_name = type(self).__name__ + '.pdf'
                PdfPrinter.print_book(file_name, book)
                ui.draw_ui(f'Результат в файле {file_name}')
            else:
                ui.print_book(book)
        except ValueError:
            ui.draw_ui('Ошибка формата ввода. Введите число.')
        except DoesNotExist:
            ui.draw_ui('Не удалось отобразить книгу. Книга с данным id не существует.')

        ui.confirm_input()
        state_manager.change_state(States.Main)


class PrintAllState(StateWithStats):
    def handle_input(self, state_manager):
        books = state_manager.book_rep.get_all()

        if ui.is_pdf():
            file_name = type(self).__name__ + '.pdf'
            PdfPrinter.print_books(file_name, books)
            ui.draw_ui(f'Результат в файле {file_name}')
        else:
            ui.print_books(books)
        ui.confirm_input()
        state_manager.change_state(States.Main)


class ExitState(StateWithStats):
    def handle_input(self, state_manager):
        state_manager.stop_work()


class StateManager:
    def __init__(self, book_rep: BookRep):
        self.state_changed = Event()
        self.__current_state = None
        self.book_rep = book_rep
        self.is_work = True

    @property
    def current_state(self):
        return self.__current_state

    def stop_work(self):
        self.is_work = False

    def change_state(self, state: State):
        if state == self.current_state:
            ui.confirm_input()
        else:
            self.__current_state = state
        ui.clear()
        string_state = self.__current_state.to_string(self)
        self.state_changed.invoke(string_state)


class States:
    Main = MainState(f'Сейчас в библиотеке %s книг(а).', [
        Command(Actions.Exit, 'выхода'),
        Command(Actions.AddBook, 'добавления книги'),
        Command(Actions.RemoveBook, 'удаления книги'),
        Command(Actions.EditBook, 'редактирования книги'),
        Command(Actions.FindBook, 'поиска книги'),
        Command(Actions.PrintAt, 'вывода детальной информации о книге'),
        Command(Actions.PrintAll, 'вывода всех книг')
    ])

    AddBook = AddBookState('Задайте параметры новой книги:', [
        Command(Actions.SetTitle, 'установки название книги'),
        Command(Actions.SetAuthor, 'установки автора книги'),
        Command(Actions.SetYear, 'установки года издания книги'),
        Command(Actions.ClearParams, 'очистки параметров'),
        Command(Actions.Execute, 'выполнения команды'),
        Command(Actions.Back, 'выхода'),
    ])

    FindBook = FindBookState('Задайте параметры для поиска книг:', [
        Command(Actions.SetTitle, 'установки название книги'),
        Command(Actions.SetAuthor, 'установки автора книги'),
        Command(Actions.SetYear, 'установки года издания книги'),
        Command(Actions.ClearParams, 'очистки параметров'),
        Command(Actions.Execute, 'выполнения команды'),
        Command(Actions.Back, 'выхода'),
    ])

    RemoveBook = RemoveBookState('Введите id книги для удаления:', [
        Command(Actions.Back, 'выхода из меню добавления'),
    ])

    EditBook = EditBookState('Введите параметры книги для редактирования:', [
        Command(Actions.SetTitle, 'установки название книги'),
        Command(Actions.SetAuthor, 'установки автора книги'),
        Command(Actions.SetYear, 'установки года издания книги'),
        Command(Actions.ClearParams, 'очистки параметров'),
        Command(Actions.Execute, 'выполнения команды'),
        Command(Actions.Back, 'выхода из меню редактирования'),
    ])

    Print = PrintState('Введите id книги для отображения:', [
        Command(Actions.Back, 'для выхода из меню добавления'),
    ])

    PrintAll = PrintAllState(f'Сейчас в библиотеке %s книг.', [])

    Exit = ExitState(f'Сейчас в библиотеке %s книг. Выход из библиотеки.', [])
