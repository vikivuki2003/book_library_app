
import json
from typing import List, Optional
from book import Book

class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self) -> List[Book]:
        """Загружает книги из файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return [Book(**book_data) for book_data in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            print("Ошибка чтения файла или данные повреждены.")
            return []

    def save_books(self) -> None:
        """Сохраняет книги в файл."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.to_dict() for book in self.books], file, ensure_ascii=False)

    def add_book(self, book: Book) -> None:
        """Добавляет книгу и сохраняет изменения."""
        self.books.append(book)
        self.save_books()

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу по ID и сохраняет изменения."""
        book_to_remove = next((book for book in self.books if book.id == book_id), None)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            return True
        return False

    def find_books(self, id: Optional[int] = None, title: Optional[str] = None,
                   author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
        """Ищет книги по заданным параметрам."""
        results = self.books
        filters = {
            'id': (lambda b: b.id == id) if id is not None else None,
            'title': (lambda b: title.lower() in b.title.lower()) if title else None,
            'author': (lambda b: author.lower() in b.author.lower()) if author else None,
            'year': (lambda b: b.year == year) if year is not None else None
        }

        for condition in filters.values():
            if condition:
                results = [book for book in results if condition(book)]

        return results

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги по ID."""
        if status not in ['в наличии', 'выдана']:
            print(f"Ошибка: статус должен быть 'в наличии' или 'выдана'.")
            return False

        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                return True
        return False