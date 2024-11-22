class Book:
    def __init__(self, book_id: int, title: str, author: str, year: int, status: str = 'в наличии') -> None:
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def __str__(self):
        return f"{self.id}: {self.title} by {self.author}, {self.year} ({self.status})"