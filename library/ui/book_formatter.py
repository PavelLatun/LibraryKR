from model.book import Book


class BookFormatter:

    @staticmethod
    def format_books(books):
        book_list = ''

        for book in books:
            book_list += f'{BookFormatter.format_book(book)}\n'

        return book_list

    @staticmethod
    def format_book(book):
        return f'{book[0]} - {book[1].title}, {book[1].year}, {book[1].author}'
