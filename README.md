# Система управления библиотекой  

**Система управления библиотекой** — это простое приложение командной строки, которое позволяет пользователям управлять библиотечным фондом книг. Пользователи могут добавлять, искать, обновлять, удалять и просматривать книги в библиотеке.  

## Возможности  

- **Добавление книги**: Пользователи могут вводить такие данные, как название, автор и год издания, чтобы добавить новые книги в библиотеку.  
- **Поиск книг**: Пользователи могут искать книги по названию, автору или году издания.  
- **Обновление статуса книги**: Пользователи могут обновлять статус доступности книг (например, "в наличии" или "выдана").  
- **Удаление книги**: Пользователи могут удалять книги из библиотеки по их идентификатору (ID).  
- **Просмотр всех книг**: Пользователи могут отображать все книги, доступные в библиотеке.  

## Зависимости  

- Python 3.6 или выше  
- `json` (включен в стандартную библиотеку Python)  
- Убедитесь, что файл `books.json` существует в той же директории, чтобы сохранять данные о книгах.  

## Установка  

1. Клонируйте репозиторий:  
   git clone https://github.com/ваш_логин/library-management-system.git  
   cd library-management-system  

Убедитесь, что у вас есть файл books.json. Если его нет, приложение создаст его автоматически при добавлении первой книги.

## Использование
Запустите приложение:
python main.py

Следуйте подсказкам на экране для управления библиотекой:

Выберите опцию из меню, введя соответствующий номер (1-6).
Введите необходимую информацию для выбранной опции.
Чтобы выйти из приложения, выберите опцию выхода из меню.
