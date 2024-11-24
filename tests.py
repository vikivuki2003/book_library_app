import json
import unittest
from unittest.mock import MagicMock, patch, mock_open
from library import Library, Storage, Book
from book_manager import BookManager


class TestLibrary(unittest.TestCase):
    def setUp(self):
        self.storage = MagicMock()
        self.library = Library(self.storage)

    def test_get_next_id(self):
        self.storage.books = [Book(1, 'Книга 1', 'Автор 1', 2021)]
        self.assertEqual(self.library.get_next_id(), 2)

    def test_add_book_success(self):
        self.storage.find_books.return_value = []
        self.library.add_book("Тестовая Книга", "Автор", 2023)
        self.storage.add_book.assert_called_once()

    def test_remove_book_success(self):
        book = Book(1, "Книга 1", "Автор 1", 2021)
        self.storage.books = [book]
        self.storage.remove_book.return_value = True

        result = self.library.remove_book(1)
        self.assertTrue(result)
        self.storage.remove_book.assert_called_once_with(1)

    def test_find_books(self):
        book = Book(1, "Тестовая Книга", "Автор", 2021)
        self.storage.find_books.return_value = [book]

        results = self.library.find_books(title="Тестовая Книга")
        self.assertIn(book, results)

    def test_update_book_status_success(self):
        book = Book(1, "Книга", "Автор", 2023, "выдана")
        self.storage.books = [book]

        self.library.update_book_status(1, "в наличии")
        self.assertEqual(book.status, "в наличии")

    # Тесты для класса Storage


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.mock_filename = 'test_books.json'
        self.storage = Storage(self.mock_filename)

    @patch("builtins.open", new_callable=mock_open,
           read_data='[{"id": 1, "title": "Книга", "author": "Автор", "year": 2021}]')
    def test_load_books(self, mock_file):
        books = self.storage.load_books()
        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].title, "Книга")

    def test_load_books_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            books = self.storage.load_books()
            self.assertEqual(books, [])

    @patch('builtins.open', new_callable=mock_open)
    def test_save_books(self, mock_file):
        book = Book(1, "Тестовая Книга", "Автор", 2023)
        self.storage.books = [book]
        expected_data = json.dumps([book.to_dict()], ensure_ascii=False, indent=4)  # Используйте to_dict

        self.storage.save_books()  # Сохраните книги

        # Убедитесь, что файл открыт с правильным именем
        mock_file.assert_called_once_with('test_books.json', 'w', encoding='utf-8')

        # Убедитесь, что write был вызван один раз с ожидаемыми данными
        handle = mock_file()
        handle.write.assert_called_once_with(expected_data)


class TestBookManager(unittest.TestCase):
    def setUp(self):
        self.library = MagicMock(spec=Library)
        self.book_manager = BookManager(self.library)

    @patch('builtins.input', side_effect=['Тестовая Книга', 'Автор', '2023'])
    def test_add_book_success(self, mock_input):
        self.library.add_book.return_value = None
        with patch('builtins.print') as mock_print:
            self.book_manager.add_book()
            mock_print.assert_called_once_with("Книга добавлена!")
            self.library.add_book.assert_called_once_with('Тестовая Книга', 'Автор', 2023)

    @patch('builtins.input', side_effect=['', 'Автор', '2023'])
    def test_add_book_missing_fields(self, mock_input):
        with patch('builtins.print') as mock_print:
            self.book_manager.add_book()
            mock_print.assert_called_once_with(
                "Ошибка: Все поля должны быть заполнены. Пожалуйста, введите название, автора и год.")

    @patch('builtins.input', side_effect=['Тестовая Книга', 'Автор', '2021'])  # Убедитесь, что здесь три значения
    def test_search_book_success(self, mock_input):
        book = Book(1, "Тестовая Книга", "Автор", 2021)
        self.library.find_books.return_value = [book]

        with patch('builtins.print') as mock_print:
            self.book_manager.search_book()
            mock_print.assert_any_call("Найденные книги:")
            mock_print.assert_any_call(
                f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status}")

    @patch('builtins.input', side_effect=['999'])
    def test_remove_book_success(self, mock_input):
        self.library.remove_book.return_value = True

        with patch('builtins.print') as mock_print:
            self.book_manager.remove_book()
            mock_print.assert_called_once_with("Книга с ID 999 удалена.")

    @patch('builtins.input', side_effect=['999'])
    def test_remove_book_not_found(self, mock_input):
        self.library.remove_book.return_value = False

        with patch('builtins.print') as mock_print:
            self.book_manager.remove_book()
            mock_print.assert_called_once_with("Книга с ID 999 не найдена.")


if __name__ == '__main__':
    unittest.main()