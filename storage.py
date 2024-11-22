import json
from typing import List, Optional
from book import Book

class Storage:
    def __init__(self, filename: str):
        self.filename = filename
        self.books = self.load_books()

    def load_books(self) -> List[Book]:
        """Загружает книги из файла JSON."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                return [Book(**book) for book in data]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка загрузки книг: {e}")
            return []

    def save_books(self) -> None:
        """Сохраняет книги в файл JSON."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            json.dump([book.__dict__ for book in self.books], file, ensure_ascii=False, indent=4)

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

    def find_books(self, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[
        Book]:
        """Ищет книги по заголовку, автору или году."""
        results = self.books
        if title:
            results = [book for book in results if title.lower() in book.title.lower()]
        if author:
            results = [book for book in results if author.lower() in book.author.lower()]
        if year:
            results = [book for book in results if book.year == year]
        return results

    def update_status(self, book_id: int, status: str) -> bool:
        """Обновляет статус книги по ID."""
        for book in self.books:
            if book.id == book_id:
                book.status = status
                self.save_books()
                return True
        return False