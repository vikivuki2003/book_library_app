from storage import Storage
from library import Library

def main():
    storage = Storage('books.json')
    library = Library(storage)

    while True:
        print("\nМеню:")
        print("1. Добавить книгу")
        print("2. Показать все книги")
        print("3. Найти книги по автору")
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
            author = input("Введите автора для поиска: ")
            found_books = library.find_books(author=author)
            if found_books:
                print("Найденные книги:")
                for book in found_books:
                    print(book)
            else:
                print("Книги не найдены.")

        elif choice == '4':
            book_id = int(input("Введите ID книги для обновления статуса: "))
            status = input("Введите новый статус книги: ")
            if library.update_status(book_id, status):
                print("Статус обновлен!")
            else:
                print("Книга не найдена.")

        elif choice == '5':
            book_id = int(input("Введите ID книги для удаления: "))
            if library.remove_book(book_id):
                print("Книга удалена!")
            else:
                print("Книга не найдена.")

        elif choice == '6':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()