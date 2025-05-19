# Library Management System in Python

import json
import datetime
import os

# Global file paths
BOOKS_FILE = 'books.json'
MEMBERS_FILE = 'members.json'
TRANSACTIONS_FILE = 'transactions.json'

# Utility Functions

def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def save_data(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Book Class
class Book:
    def __init__(self, book_id, title, author, year):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.year = year

    def to_dict(self):
        return self.__dict__

# Member Class
class Member:
    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    def to_dict(self):
        return self.__dict__

# Transaction Class
class Transaction:
    def __init__(self, transaction_id, book_id, member_id, issue_date, return_date=None):
        self.transaction_id = transaction_id
        self.book_id = book_id
        self.member_id = member_id
        self.issue_date = issue_date
        self.return_date = return_date

    def to_dict(self):
        return self.__dict__

# Library Management Class
class Library:
    def __init__(self):
        self.books = load_data(BOOKS_FILE)
        self.members = load_data(MEMBERS_FILE)
        self.transactions = load_data(TRANSACTIONS_FILE)

    # Book Management
    def add_book(self, title, author, year):
        book_id = len(self.books) + 1
        new_book = Book(book_id, title, author, year)
        self.books.append(new_book.to_dict())
        save_data(BOOKS_FILE, self.books)
        print(f"Book '{title}' added successfully.")

    def view_books(self):
        print("\n--- All Books ---")
        for book in self.books:
            print(book)

    def delete_book(self, book_id):
        self.books = [book for book in self.books if book['book_id'] != book_id]
        save_data(BOOKS_FILE, self.books)
        print(f"Book ID {book_id} deleted successfully.")

    def search_book(self, keyword):
        print(f"\n--- Search Results for '{keyword}' ---")
        results = [b for b in self.books if keyword.lower() in b['title'].lower() or keyword.lower() in b['author'].lower()]
        for book in results:
            print(book)

    # Member Management
    def register_member(self, name):
        member_id = len(self.members) + 1
        new_member = Member(member_id, name)
        self.members.append(new_member.to_dict())
        save_data(MEMBERS_FILE, self.members)
        print(f"Member '{name}' registered successfully.")

    def view_members(self):
        print("\n--- All Members ---")
        for member in self.members:
            print(member)

    # Transaction Management
    def issue_book(self, book_id, member_id):
        transaction_id = len(self.transactions) + 1
        issue_date = datetime.date.today().isoformat()
        new_transaction = Transaction(transaction_id, book_id, member_id, issue_date)
        self.transactions.append(new_transaction.to_dict())
        save_data(TRANSACTIONS_FILE, self.transactions)
        print(f"Book ID {book_id} issued to Member ID {member_id}.")

    def return_book(self, transaction_id):
        for trans in self.transactions:
            if trans['transaction_id'] == transaction_id and trans['return_date'] is None:
                trans['return_date'] = datetime.date.today().isoformat()
                save_data(TRANSACTIONS_FILE, self.transactions)
                print(f"Book returned for Transaction ID {transaction_id}.")
                return
        print("Transaction not found or already returned.")

    def view_transactions(self):
        print("\n--- All Transactions ---")
        for trans in self.transactions:
            print(trans)

# Main Menu

def main():
    library = Library()

    while True:
        print("""
======== Library Management System ========
1. Add Book
2. View Books
3. Delete Book
4. Search Book
5. Register Member
6. View Members
7. Issue Book
8. Return Book
9. View Transactions
0. Exit
        """)
        choice = input("Enter your choice: ")

        if choice == '1':
            ti
