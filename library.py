import json
from typing import Optional

from book import Book
from storage import Storage

class Library:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get_next_id(self) -> int:
        """Возвращает следующий доступный идентификатор для новой книги."""
        return max((book.id for book in self.storage.books), default=0) + 1

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет новую книгу в библиотеку, если она еще не существует."""
        existing_books = self.storage.find_books(title=title, author=author)

        if existing_books:
            print(f"Ошибка: Книга '{title}' автором '{author}' уже существует в библиотеке.")
            return

        book = Book(self.get_next_id(), title, author, year)
        self.storage.add_book(book)
        print(f"Книга '{title}' добавлена.")

    def remove_book(self, book_id: int) -> None:
        """Удаляет книгу из библиотеки по ID."""
        if self.storage.remove_book(book_id):
            print(f"Книга с ID {book_id} удалена.")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def find_books(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> None:
        """Ищет книги по заголовку, автору или году и выводит результаты."""
        results = self.storage.find_books(title, author, year)
        if results:
            for book in results:
                print(book)
        else:
            print("Книги не найдены.")

    def display_books(self) -> None:
        """Отображает все книги в библиотеке."""
        if not self.storage.books:
            print("В библиотеке нет книг.")
            return

        for book in self.storage.books:
            print(book)

    def update_status(self, book_id: int, status: str) -> None:
        """Обновляет статус книги по ID."""
        if self.storage.update_status(book_id, status):
            print(f"Статус книги с ID {book_id} обновлен на '{status}'.")
        else:
            print(f"Книга с ID {book_id} не найдена.")