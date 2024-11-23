import unittest
from unittest.mock import patch, MagicMock
from library import Library
from storage import Storage
from book import Book
from book_manager import BookManager

class TestLibrary(unittest.TestCase):

    def setUp(self):
        """Настройка для тестирования: создание имитации хранилища и библиотеки."""
        self.storage = MagicMock(spec=Storage)
        self.library = Library(self.storage)

    def test_get_next_id_no_books(self):
        """Тест на получение следующего ID, когда книг нет."""
        self.storage.books = []
        self.assertEqual(self.library.get_next_id(), 1)

    def test_get_next_id_with_books(self):
        """Тест на получение следующего ID, когда книги присутствуют."""
        self.storage.books = [Book(1, "Книга 1", "Автор 1", 2021)]
        self.assertEqual(self.library.get_next_id(), 2)

    def test_add_book_success(self):
        """Тест на добавление книги в библиотеку."""
        self.storage.find_books.return_value = []
        self.storage.add_book.side_effect = None

        with patch('builtins.print') as mock_print:
            self.library.add_book("Тестовая Книга", "Автор", 2023)
            mock_print.assert_called_once_with("Книга 'Тестовая Книга' добавлена.")

    def test_add_book_already_exists(self):
        """Тест на добавление уже существующей книги."""
        book = Book(1, "Тестовая Книга", "Автор", 2023)
        self.storage.find_books.return_value = [book]

        with patch('builtins.print') as mock_print:
            self.library.add_book("Тестовая Книга", "Автор", 2023)
            mock_print.assert_called_once_with("Ошибка: Книга 'Тестовая Книга' автором 'Автор' уже существует.")

    def test_remove_book_success(self):
        """Тест на удаление книги."""
        self.storage.remove_book.return_value = True

        result = self.library.remove_book(1)
        self.assertTrue(result)

    def test_remove_book_failure(self):
        """Тест на неудачное удаление книги."""
        self.storage.remove_book.return_value = False

        result = self.library.remove_book(2)
        self.assertFalse(result)

    def test_find_books_success(self):
        """Тест на поиск книг, когда книги найдены."""
        book = Book(1, "Тестовая Книга", "Автор", 2021)
        self.storage.find_books.return_value = [book]

        results = self.library.find_books(title="Тестовая Книга")
        self.assertIn(book, results)

    def test_find_books_no_results(self):
        """Тест на поиск книг, когда книги не найдены."""
        self.storage.find_books.return_value = []

        results = self.library.find_books(title="Неизвестная Книга")
        self.assertEqual(results, [])


class TestStorage(unittest.TestCase):

    def setUp(self):
        """Настройка для тестирования хранилища."""
        self.storage = Storage('test_books.json')
        self.storage.books = []

    def test_add_book(self):
        """Тест на добавление книги."""
        book = Book(1, "Тестовая Книга", "Автор", 2023)
        with patch.object(self.storage, 'save_books') as mock_save:
            self.storage.add_book(book)
            self.assertIn(book, self.storage.books)
            mock_save.assert_called_once()

    def test_remove_book_success(self):
        """Тест на удаление книги."""
        book = Book(1, "Тестовая Книга", "Автор", 2023)
        self.storage.books.append(book)

        result = self.storage.remove_book(1)
        self.assertTrue(result)
        self.assertNotIn(book, self.storage.books)

    def test_remove_book_failure(self):
        """Тест на неудачное удаление книги."""
        book = Book(1, "Тестовая Книга", "Автор", 2023)
        self.storage.books.append(book)

        result = self.storage.remove_book(2)  # 2 не существует
        self.assertFalse(result)

    def test_find_books(self):
        """Тест на поиск книг с учетом различных параметров."""
        book1 = Book(1, "Книга Первая", "Автор Первый", 2021)
        book2 = Book(2, "Книга Вторая", "Автор Второй", 2022)
        self.storage.books = [book1, book2]

        results = self.storage.find_books(title="Книга Первая")
        self.assertIn(book1, results)
        self.assertNotIn(book2, results)

        results = self.storage.find_books(author="Автор Второй")
        self.assertIn(book2, results)
        self.assertNotIn(book1, results)

    def test_find_books_empty(self):
        """Тест на поиск, когда книги отсутствуют."""
        results = self.storage.find_books(title="Неизвестная Книга")
        self.assertEqual(results, [])


class TestBookManager(unittest.TestCase):

    def setUp(self):
        """Настройка для тестирования менеджера книг."""
        self.manager = BookManager()
        self.manager.library = MagicMock(spec=Library)

    @patch('builtins.input', side_effect=['1', 'в наличии'])
    def test_update_book_status_success(self, mock_input):
        """Тест на успешное обновление статуса книги."""
        self.manager.library.get_book_status.return_value = Book(1, "Книга", "Автор", 2023, "выдана")
        self.manager.library.update_book_status.return_value = None

        with patch('builtins.print') as mock_print:
            self.manager.update_book_status()
            self.manager.library.update_book_status.assert_called_once_with(1, "в наличии")
            mock_print.assert_called_once_with("Статус книги с ID 1 обновлен на 'в наличии'.")

    @patch('builtins.input', side_effect=['1', 'неверный статус'])
    def test_update_book_status_invalid(self, mock_input):
        """Тест на попытку обновления статуса книги на недопустимый статус."""
        self.manager.library.get_book_status.return_value = Book(1, "Книга", "Автор", 2023, "выдана")

        with patch('builtins.print') as mock_print:
            self.manager.update_book_status()
            mock_print.assert_called_once_with("Ошибка: статус должен быть 'в наличии' или 'выдана'.")

    @patch('builtins.input', side_effect=['1'])
    def test_remove_book_success(self, mock_input):
        """Тест на успешное удаление книги."""
        self.manager.library.remove_book.return_value = True

        with patch('builtins.print') as mock_print:
            self.manager.remove_book()
            mock_print.assert_called_once_with("Книга с ID 1 удалена.")

    @patch('builtins.input', side_effect=['2'])
    def test_remove_book_failure(self, mock_input):
        """Тест на неудачное удаление книги."""
        self.manager.library.remove_book.return_value = False

        with patch('builtins.print') as mock_print:
            self.manager.remove_book()
            mock_print.assert_called_once_with("Книга с ID 2 не найдена.")

    def test_show_all_books(self):
        """Тест на отображение всех книг в библиотеке."""
        book = Book(1, "Книга", "Автор", 2023)
        self.manager.library.get_all_books.return_value = [book]

        with patch('builtins.print') as mock_print:
            self.manager.show_all_books()
            mock_print.assert_called_once_with("Список всех книг:")

    def test_show_all_books_empty(self):
        """Тест на отображение, когда книг нет."""
        self.manager.library.get_all_books.return_value = []

        with patch('builtins.print') as mock_print:
            self.manager.show_all_books()
            mock_print.assert_called_once_with("В библиотеке нет книг.")


if __name__ == '__main__':
    unittest.main()