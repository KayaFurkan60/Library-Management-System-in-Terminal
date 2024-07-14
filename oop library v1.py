class Book:
    def __init__(self, title, author, isbn, genre):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.available = True

    def check_out(self, member_id, due_date):
        if self.available:
            self.available = False
            return f"The book {self.title}, has been booked by {member_id} . Return date: {due_date}"
        else:
            return f"The book is currently borrowed by another member."

    def check_in(self):
        if not self.available:
            self.available = True
            return f"The '{self.title}'book was returned successfully."
        else:
            return "The book is already in the library."

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def display_books(self):
        for i, book in enumerate(self.books, start=1):
            print(f"{i}. Title: {book.title}, Author: {book.author}")

library = Library()

# Add books to library
book1 = Book("Python Crash Course", "Eric Matthes", "978-1593276034", "Programming")
book2 = Book("Sapiens", "Yuval Noah Harari", "978-0062316097", "History")
book3 = Book("1984", "George Orwell", "978-0451524935", "Fiction")

library.add_book(book1)
library.add_book(book2)
library.add_book(book3)
library.display_books()


selected_book_index = int(input("Which book would you like to buy? (Enter book number): ")) - 1 #-1 is for list format
selected_book = library.books[selected_book_index]


member_id = input("Library Member Code: ")
due_date = input("Return Date (YYYY-MM-DD): ")


result = selected_book.check_out(member_id, due_date)
print(result)

