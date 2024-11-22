import json
from typing import List, Optional
from book import Book


class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self) -> List:
        """Загружает книги из файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return [Book(**book_data) for book_data in json.load(file)]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Ошибка чтения файла. Данные могут быть повреждены.")
            return []

    def save_books(self) -> None:
        """Сохраняет список книг в файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False)

    def add_book(self, book: Book) -> None:
        """Добавляет книгу в список и сохраняет в файл."""
        self.books.append(book)
        self.save_books()

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу из списка по ID и сохраняет изменения."""
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            return True
        return False

    def find_books(self, id: Optional[int] = None, title: Optional[str] = None, author: Optional[str] = None,
                   year: Optional[int] = None) -> list:
        """Ищет книги по ID, заголовку, автору или году."""

        try:
            results = self.books
            if id is not None:
                results = [book for book in results if book.id == id]
            if title:
                results = [book for book in results if title.lower() in book.title.lower()]
            if author:
                results = [book for book in results if author.lower() in book.author.lower()]
            if year is not None:
                results = [book for book in results if book.year == year]
            return results

        except Exception as e:
            print(f"Произошла ошибка при поиске книг: {e}")
            return []

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги по ID."""
        valid_statuses = ['в наличии', 'выдана']
        if status not in valid_statuses:
            print(f"Ошибка: статус должен быть одним из следующих: {valid_statuses}.")
            return False

        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                return True
        return False