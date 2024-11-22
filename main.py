from storage import Storage
from library import Library
from book_manager import BookManager

def main():
    storage = Storage('books.json')
    library = Library(storage)
    manager = BookManager(library)

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
            manager.add_book()
        elif choice == '2':
            manager.show_all_books()
        elif choice == '3':
            manager.search_book()
        elif choice == '4':
            manager.update_status()
        elif choice == '5':
            manager.remove_book()
        elif choice == '6':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

        input("\nНажмите Enter, чтобы вернуться в меню...")

if __name__ == "__main__":
    main()