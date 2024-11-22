from storage import Storage
from library import Library

def main():
    storage = Storage('books.json')
    library = Library(storage)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книгу")
        print("4. Обновить статус книги")
        print("5. Удалить книгу")
        print("6. Выход")

        choice = input("Выберите опцию (1-6): ")

        if choice == '1':
            title = input("Введите название книги: ")
            author = input("Введите автора книги: ")
            year = int(input("Введите год издания: "))
            library.add_book(title, author, year)
            print("Книга добавлена!")

        elif choice == '2':
            print("\nВсе книги в библиотеке:")
            library.display_books()


        elif choice == '3':

            try:
                author = input("Введите автора для поиска (можно часть фамилии или инициалы): ")
                title = input("Введите название книги для поиска (можно часть названия или оставьте пустым): ")
                year_input = input("Введите год издания (или оставьте пустым): ")
                year = int(year_input) if year_input.isdigit() else None
                found_books = library.find_books(title=title, author=author, year=year)

                if found_books:
                    print("Найденные книги:")
                    for book in found_books:
                        print(book)
            except ValueError:
                print("Ошибка: Пожалуйста, введите корректный год.")
            except Exception as e:
                print(f"Произошла ошибка: {e}")


        elif choice == '4':
            book_id = int(input("Введите ID книги для обновления статуса:  "))
            if not library.storage.find_books(id=book_id):
                print(f"Книга с ID {book_id} не найдена.")
            else:
                status = input("Введите новый статус книги. Варианты: 'в наличии' / 'выдана': ")
                library.update_book_status(book_id, status)
                print("Статус обновлен!")

        elif choice == '5':
            book_id = int(input("Введите ID книги для удаления: "))
            library.remove_book(book_id)
            print("Книга удалена!")

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

        input("\nНажмите Enter, чтобы вернуться в меню...")

if __name__ == "__main__":
    main()