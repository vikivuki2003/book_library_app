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

    def find_books(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> list:
        """Ищет книги по заголовку, автору или году и возвращает результаты."""
        try:
            results = self.storage.find_books(title, author, year)
            return results
        except Exception as e:
            print(f"Произошла ошибка при поиске книг: {e}")
            return []

    def display_books(self) -> None:
        """Отображает все книги в библиотеке."""
        if not self.storage.books:
            print("В библиотеке нет книг.")
            return

        for book in self.storage.books:
            print(book)

    def update_book_status(self, book_id: int, new_status: str) -> str:
        """Обновляет статус книги по ID."""
        valid_statuses = ['в наличии', 'выдана']
        if new_status not in valid_statuses:
            return f"Ошибка: статус должен быть одним из следующих: {valid_statuses}."

        book = next((book for book in self.books if book.id == book_id), None)
        if not book:
            return f"Книга с ID {book_id} не найдена."

        book.status = new_status
        return "Статус обновлен!"