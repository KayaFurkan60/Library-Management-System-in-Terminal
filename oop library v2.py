#first of all we need to import some libraries
import yaml
from datetime import datetime, timedelta

"""
In this exammple we will use yaml library to load the data from a yaml file
The .yaml file is a data file. It is a data serialization format that is human-readable and machine-processable.
It is very easy to read and data can be added and removed very easily.
alo we use datetime library to get the current date and time and to add some days to it.
"""


#creating a class for the book
class Book:
    def __init__(self, title, author, isbn, place, code):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = place
        self.code = code
        self.available = True  # Is the book currently available in the library?
        self.reserved_by = None
        self.due_date = None

    def check_out(self, member_id, due_date):
        if self.available and not self.reserved_by:
            self.available = False
            self.reserved_by = member_id
            self.due_date = datetime.strptime(due_date, "%Y-%m-%d")
            return f"The book '{self.title}' has been checked out by member {member_id}. Due date: {due_date}"
        elif self.reserved_by:
            return f"The book '{self.title}' has already been reserved by {self.reserved_by}."
        else:
            return f"The book '{self.title}' is currently checked out by another member."

    def check_in(self):
        if not self.available:
            reserved_by = self.reserved_by
            self.available = True
            self.reserved_by = None
            self.due_date = None
            return f"The book '{self.title}' has been successfully returned. It is now available in the library."
        else:
            return "The book is already in the library."

#creating a class for the library
class Library:
    def __init__(self):
        self.books_by_genre = {}
        self.user_data = {}

    def load_from_yaml(self, filename, user_filename):
        with open(filename, 'r', encoding='utf-8') as file:
            data = yaml.safe_load(file)
            if data:
                for genre, books_data in data.items():
                    books = [Book(book["title"], book["author"], book["isbn"], book["place"], book["code"]) for book in books_data]
                    self.books_by_genre[genre] = books

        with open(user_filename, 'r', encoding='utf-8') as user_file:
            user_data = yaml.safe_load(user_file)
            if user_data:
                self.user_data = user_data

    def get_book_by_code(self, code):
        for genre, books in self.books_by_genre.items():
            for book in books:
                if book.code == code:
                    return book
        return None
        

    def reserve_book(self, book, member_id, due_date):
        if "reserved_books" not in self.user_data:
            self.user_data["reserved_books"] = {}

        if book.code not in self.user_data["reserved_books"]:
            self.user_data["reserved_books"][book.code] = {"member_id": member_id, "due_date": due_date}
            book.check_out(member_id, due_date)
            result = f"The book '{book.title}' has been successfully reserved until {due_date}."
        else:
            reserved_by = self.user_data["reserved_books"][book.code]["member_id"]
            result = f"The book '{reserved_by}' has already been reserved until {self.user_data['reserved_books'][book.code]['due_date']}."

        with open("user_data.yaml", 'w', encoding='utf-8') as user_file:
            yaml.dump(self.user_data, user_file, default_flow_style=False)

        return result

# Example usage:
library = Library()
library.load_from_yaml("library_data.yaml", "user_data.yaml")

#there is a while true loop to ask the user to enter the book code for continually
while True:
    # Ask which book to reserve
    selected_code = input("Which book would you like to reserve? (Enter the book code, 'q' to exit): ")
    
    if selected_code.lower() == 'q':
        print("Exiting...")
        break  # End the loop

    selected_book = library.get_book_by_code(selected_code)

    # If the selected book exists, perform the operations
    if selected_book:
        member_id = input("Library Member ID: ")
        # Check if the user code is valid
        assert str(member_id) in library.user_data.values(), "This user code is not valid. Please enter a correct user code."
        due_date = input("Return Date (YYYY-MM-DD): ")
        # Reserve the book and show the result
        result = library.reserve_book(selected_book, member_id, due_date)
        print(result)
    else:
        print("Book not found.")
