from datetime import datetime, timedelta

import json
import pytest

from flaskr import db
from flaskr import create_app
from flaskr import init_db
from flaskr.library.Book import Book
from flaskr.library.Copy import Copy
from flaskr.library.Loan import Loan
from flaskr.library.Member import Member
from flaskr.library.Author import Author

# define Member type variable


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    # create the database and load test data
    # set _password to pre-generated hashes, since hashing for each test is slow
    with app.app_context():
        init_db()
        author = Author(nickname="John Smith0",
                        first_name="John", last_name="Smith")
        db.session.add(author)
        book = Book(title="My Book", author=author, ISBN="1234567890",
                    publication_date='2000-11-11', genre="Test Genre1")
        member = Member(first_name="Jane", last_name="Doe",
                        email="aa@example.com", password="123456", is_admin=False)
        db.session.add(book)
        db.session.add(member)

        db.session.commit()

    yield app


def test_author_created(app):

    with app.app_context():
        # get the generated author
        author = db.session.get(Author, 1)
        assert author.nickname == "John Smith0"
        assert author.id == 1


def test_book_created_with_author(app):
    with app.app_context():
        # get the first author:
        author = db.session.query(Author).first()
        # get the first book:
        book = db.session.query(Book).first()
        # assert that the author of the book is the same as the author
        assert book.author == author


def test_copy_created_with_book(app):

    with app.app_context():
        book = db.session.get(Book, 1)
        copy = Copy(location="Library 1", book=book)
        db.session.add(copy)

        db.session.commit()

        assert copy.book == book


def test_loan_created_with_copy_and_member(app):

    with app.app_context():
        book = db.session.get(Book, 1)
        member = db.session.get(Member, 1)

        copy = Copy(location="Library 1", book=book)
        db.session.add(copy)
        db.session.commit()

        loan = Loan(copy=copy, member=member,
                    loan_date=datetime.now(), due_date=datetime.now() + timedelta(days=14))
        db.session.add(member)
        db.session.add(loan)
        db.session.commit()

        assert loan.copy == copy
        assert loan.member == member
