import operator
from functools import reduce

from db.book import BookModel
from model.book import Book
from peewee import MySQLDatabase


class BookRep:
    def __init__(self, data_base=MySQLDatabase('library', user='root', password='pass',
                                               host='localhost', port=3306)):
        self.__data_base = data_base
        self.__library_model = BookModel()
        self.__library_model._meta.database = self.__data_base  # type: ignore

    @staticmethod
    def __get_book(book):
        new_book = Book()

        new_book.year = book.year
        new_book.title = book.title
        new_book.author = book.author

        return new_book

    @staticmethod
    def __get_books(books):
        book_list = []
        for book in books:
            new_book = BookRep.__get_book(book)

            book_list.append(
                (
                    book.id,
                    new_book
                )
            )
        return book_list

    def remove_at(self, index: int):
        self.__library_model.get_by_id(index).delete_instance()

    def get_at(self, index: int):
        return index, self.__get_book(self.__library_model.get_by_id(index))

    def update_at(self, index, book: Book):
        instance: BookModel
        instance = self.__library_model.get_by_id(index)

        if book.year:
            instance.year = book.year  # type: ignore
        if book.author:
            instance.author = book.author  # type: ignore
        if book.title:
            instance.title = book.title  # type: ignore

        instance.save()

    def connect(self):
        self.__data_base.connect()

    def close(self):
        self.__data_base.close()

    def add(self, book: Book):
        self.__library_model.create(
            author=book.author,
            year=book.year,
            title=book.title
        )

    def find_by_author(self, author):
        query = self.__library_model.select().where(BookModel.author == author)
        return self.__get_books(query)

    def find_by_year(self, year):
        query = self.__library_model.select().where(BookModel.year == year)
        return self.__get_books(query)

    def find(self, book: Book):
        clauses = []

        if book.year:
            clauses.append(BookModel.year == book.year)
        if book.author:
            clauses.append(BookModel.author.contains(book.author))
        if book.title:
            clauses.append(BookModel.title.contains(book.title))

        return self.__get_books(self.__library_model.select().where(reduce(operator.and_, clauses)))

    def count(self):
        return self.__library_model.select().count()

    def get_all(self):
        query = self.__library_model.select()
        return self.__get_books(query)
