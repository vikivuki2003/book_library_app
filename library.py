from typing import Optional, List
from book import Book
from storage import Storage

class Library:
    def __init__(self, storage: Storage):
        self.storage = storage

    def get_next_id(self) -> int:
        return max((book.id for book in self.storage.books), default=0) + 1

    def add_book(self, title: str, author: str, year: int) -> None:
        """Добавляет книгу в библиотеку."""
        if self.storage.find_books(title=title, author=author):
            print(f"Ошибка: Книга '{title}' автором '{author}' уже существует.")
            return

        book = Book(self.get_next_id(), title, author, year)
        self.storage.add_book(book)
        print(f"Книга '{title}' добавлена.")

    def remove_book(self, book_id: int) -> bool:
        """Удаляет книгу и возвращает True, если книга была удалена, иначе False."""
        return self.storage.remove_book(book_id)

    def find_books(self, title: Optional[str] = None,
                   author: Optional[str] = None,
                   year: Optional[int] = None) -> List[Book]:
        return self.storage.find_books(title=title, author=author, year=year)

    def get_all_books(self) -> List[Book]:
        """Возвращает все книги в библиотеке."""
        return self.storage.books

    def update_book_status(self, book_id: int, new_status: str) -> None:
        """Обновляет статус книги, если она существует."""
        book = self.get_book_status(book_id)
        if book is not None:
            valid_statuses = ['в наличии', 'выдана']
            if new_status in valid_statuses:
                book.status = new_status
                print(f"Статус книги с ID {book_id} обновлен на '{new_status}'.")
            else:
                print(f"Неверный статус: '{new_status}'. Доступные статусы: {', '.join(valid_statuses)}")
        else:
            print(f"Книга с ID {book_id} не найдена.")

    def get_book_status(self, book_id: int) -> Optional[Book]:
        for book in self.storage.books:
            if book.id == book_id:
                return book
        return None