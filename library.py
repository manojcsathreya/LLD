from typing import List, Dict, Optional
from enum import Enum
from collections import defaultdict
from datetime import date, timedelta

# Book Class
class Book:
    def __init__(self, isbn: str, title: str, author: str, publication_year: int):
        self._isbn = isbn
        self._title = title
        self._author = author
        self._publication_year = publication_year
        self._available = True

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def publication_year(self) -> int:
        return self._publication_year

    @property
    def available(self) -> bool:
        return self._available

    @available.setter
    def available(self, available: bool):
        self._available = available

# Member Class
class Member:
    def __init__(self, member_id: str, name: str, contact_info: str):
        self._member_id = member_id
        self._name = name
        self._contact_info = contact_info
        self._borrowed_books: List[Book] = []

    @property
    def member_id(self) -> str:
        return self._member_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def contact_info(self) -> str:
        return self._contact_info

    @property
    def borrowed_books(self) -> List[Book]:
        return self._borrowed_books

    def borrow_book(self, book: Book):
        self._borrowed_books.append(book)

    def return_book(self, book: Book):
        self._borrowed_books.remove(book)

# Singleton Library Manager Class
class LibraryManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.catalog: Dict[str, Book] = {}
            cls._instance.members: Dict[str, Member] = {}
            cls._instance.MAX_BOOKS_PER_MEMBER = 5
            cls._instance.LOAN_DURATION_DAYS = 14
        return cls._instance

    @staticmethod
    def get_instance():
        if LibraryManager._instance is None:
            LibraryManager()
        return LibraryManager._instance

    def add_book(self, book: Book):
        self.catalog[book.isbn] = book

    def remove_book(self, isbn: str):
        self.catalog.pop(isbn, None)

    def get_book(self, isbn: str) -> Optional[Book]:
        return self.catalog.get(isbn)

    def register_member(self, member: Member):
        self.members[member.member_id] = member

    def unregister_member(self, member_id: str):
        self.members.pop(member_id, None)

    def get_member(self, member_id: str) -> Optional[Member]:
        return self.members.get(member_id)

    def borrow_book(self, member_id: str, isbn: str):
        member = self.get_member(member_id)
        book = self.get_book(isbn)

        if member and book and book.available:
            if len(member.borrowed_books) < self.MAX_BOOKS_PER_MEMBER:
                member.borrow_book(book)
                book.available = False
                print(f"Book borrowed: {book.title} by {member.name}")
            else:
                print(f"Member {member.name} has reached the maximum number of borrowed books.")
        else:
            print("Book or member not found, or book is not available.")

    def return_book(self, member_id: str, isbn: str):
        member = self.get_member(member_id)
        book = self.get_book(isbn)

        if member and book:
            member.return_book(book)
            book.available = True
            print(f"Book returned: {book.title} by {member.name}")
        else:
            print("Book or member not found.")

    def search_books(self, keyword: str) -> List[Book]:
        matching_books = [book for book in self.catalog.values() if keyword in book.title or keyword in book.author]
        return matching_books

# Demo Class
class LibraryManagementSystemDemo:
    @staticmethod
    def run():
        library_manager = LibraryManager.get_instance()

        # Add books to the catalog
        library_manager.add_book(Book("ISBN1", "Book 1", "Author 1", 2020))
        library_manager.add_book(Book("ISBN2", "Book 2", "Author 2", 2019))
        library_manager.add_book(Book("ISBN3", "Book 3", "Author 3", 2021))

        # Register members
        library_manager.register_member(Member("M1", "John Doe", "john@example.com"))
        library_manager.register_member(Member("M2", "Jane Smith", "jane@example.com"))

        # Borrow books
        library_manager.borrow_book("M1", "ISBN1")
        library_manager.borrow_book("M2", "ISBN2")

        # Return books
        library_manager.return_book("M1", "ISBN1")

        # Search books
        search_results = library_manager.search_books("Book")
        print("Search Results:")
        for book in search_results:
            print(f"{book.title} by {book.author}")

if __name__ == "__main__":
    LibraryManagementSystemDemo.run()
