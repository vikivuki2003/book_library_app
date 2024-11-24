from library import Library

class BookManager:
    def __init__(self, library: Library):
        self.library = library

    def add_book(self) -> None:
        """Запрашивает данные для добавления книги у пользователя."""
        title = input("Введите название книги: ")
        author = input("Введите автора книги: ")
        year_input = input("Введите год издания: ")

        if not title or not author or not year_input:
            print("Ошибка: Все поля должны быть заполнены. Пожалуйста, введите название, автора и год.")
            return

        try:
            year = int(year_input)
            self.library.add_book(title, author, year)
            print("Книга добавлена!")
        except ValueError:
            print("Ошибка: Пожалуйста, введите корректный год.")

    def search_book(self) -> None:
        """Запрашивает данные для поиска книги у пользователя."""
        author = input("Введите автора для поиска (можно часть фамилии или инициалы): ")
        title = input("Введите название книги для поиска (можно часть названия или оставьте пустым): ")
        year_input = input("Введите год издания (или оставьте пустым): ")

        year = int(year_input) if year_input.isdigit() else None
        found_books = self.library.find_books(title=title, author=author, year=year)

        if found_books:
            print("Найденные книги:")
            for book in found_books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
        else:
            print("Книги не найдены.")

    def update_status(self) -> None:
        """Запрашивает новые данные для обновления статуса книги."""
        try:
            book_id = int(input("Введите ID книги для обновления статуса: "))

            # Проверяем, существует ли книга с данным ID
            book = self.library.get_book_status(book_id)
            if book is None:
                print(f"Книга с ID {book_id} не найдена.")
                return  # Завершаем выполнение метода, если книга не найдена

            new_status = input("Введите новый статус книги. Варианты: 'в наличии' / 'выдана': ").strip()

            # Проверяем, что статус допустимый
            if new_status not in ['в наличии', 'выдана']:
                print("Ошибка: статус должен быть 'в наличии' или 'выдана'.")
                return

            if book.status == new_status:
                print(f"Статус книги с ID {book_id} уже '{new_status}'. Изменение не требуется.")
                return

            # Вызов метода обновления статуса книги
            self.library.update_book_status(book_id, new_status)

        except ValueError:
            print("Ошибка: ID должен быть числом.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def remove_book(self) -> None:
        """Запрашивает ID книги для удаления и удаляет её, если она существует."""
        try:
            book_id = int(input("Введите ID книги для удаления: "))
            if self.library.remove_book(book_id):
                print(f"Книга с ID {book_id} удалена.")
            else:
                print(f"Книга с ID {book_id} не найдена.")
        except ValueError:
            print("Ошибка: ID должен быть числом.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def show_all_books(self) -> None:
        """Показывает все книги в библиотеке."""
        books = self.library.get_all_books()
        if books:
            print("Список всех книг:")
            for book in books:
                print(f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")
        else:
            print("В библиотеке нет книг.")

    def _validate_status(self, status: str) -> None:
        """Проверяет, что статус допустимый."""
        if status not in ['в наличии', 'выдана']:
            raise ValueError("Ошибка: статус должен быть 'в наличии' или 'выдана'.")

    def update_book_status(self):
        pass