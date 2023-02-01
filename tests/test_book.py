from datetime import datetime, timedelta
import json
import pytest

from flaskr import db, init_db, create_app
from flaskr.library.Copy import Copy
from flaskr.library.Book import Book
from flaskr.library.Loan import Loan
from flaskr.library.Member import Member
from flaskr.library.Author import Author


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    with app.app_context():
        init_db()
        author = Author(nickname="John Smith1",
                        first_name="John", last_name="Smith")
        db.session.add(author)
        book = Book(title="My Book", author=author, ISBN="1234567892",
                    publication_date='2000-11-11', genre="Test Genre1")
        member = Member(first_name="Jane", last_name="Doe",
                        email="aa@example.com", password="123456", is_admin=False)
        db.session.add(book)
        db.session.add(member)

        book1 = Book(title='Test Book1 AAAA', author=author, ISBN='1234567894',
                     publication_date='2020-01-01', genre='Test Genre1')

        book2 = Book(title='Test Book2', author=author, ISBN='1234567890',
                     publication_date='2020-01-01', genre='Test Genre1')

        book1 = Book(title='Test Book1 AAA', author=author, ISBN='1234567895',
                     publication_date='2020-01-01', genre='Test Genre1')

        # create few copies of the book
        copy1 = Copy(book_id=1, available=True, location='shelf 1')
        copy2 = Copy(book_id=1, available=False, location='shelf 2')
        copy3 = Copy(book_id=1, available=False, location='shelf 3')

        db.session.add(book1)
        db.session.add(book2)

        db.session.add(copy1)
        db.session.add(copy2)
        db.session.add(copy3)
        db.session.commit()

    yield app


def test_add_book(client, auth, app):
    # create a test book
    book_data = {
        'title': 'Test Book',
        'author_id': 100,
        'ISBN': '1234567896',
        'publication_date': '2020-01-01',
        'genre': 'Test Genre1',
    }

    with app.app_context():

        # send a POST request to the /books endpoint
        response = client.post(
            '/api/books', data=json.dumps(book_data), content_type='application/json')
        # assert that the response has a 201 status code
        assert response.status_code == 201
        assert response.json['success'] == True
        assert response.json['result']['id'] > 0
        assert response.json['result']['created_at'] is not None
        assert response.json['result']['updated_at'] is not None

        # assert that the book was added to the database


def test_get_books(client, auth, app):
    with app.app_context():

        book = db.session.query(Book).first()
        # db.session.commit()

        # send a GET request to the /api/books endpoint
        response = client.get('/api/books')

        # assert that the response has a 200 status code
        assert response.status_code == 200

        # assert that the response contains the test book
        assert response.json[0]['title'] == book.to_dict()['title']


def test_get_book(client, auth, app):
    with app.app_context():

        book = db.session.query(Book).first()
        # db.session.commit()

        # send a GET request to the /api/books/<book_id> endpoint
        response = client.get(f'/api/books/{book.id}')

        # assert that the response has a 200 status code
        assert response.status_code == 200

        # assert that the response contains the test book
        assert response.json['id'] == 1
        assert response.json['ISBN'] == '1234567892'


def test_update_book(client, auth, app):
    with app.app_context():
        # add a test book to the library
        # get the book created on the

        book = db.session.query(Book).first()

        # update the test book
        update_data = {
            'title': 'Updated Test Book',
            'author_id': 101,
            'ISBN': '                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   0987654321                                                                                                                                                                      ',
            'publication_date': '2022-01-01',
            'genre': 'Test Genre2',
        }

        # send a PUT request to the /api/books/<book_id> endpoint
        response = client.put(
            f'/api/books/{book.id}', data=json.dumps(update_data), content_type='application/json')

        # assert that the response has a 200 status code
        assert response.status_code == 200
        assert response.json['success'] == True
        assert response.json['result']['title'] == update_data['title']
        assert response.json['result']['author_id'] == update_data['author_id']
        assert response.json['result']['ISBN'] == update_data['ISBN']
        assert response.json['result']['genre'] == update_data['genre']
#         # assert that the book was updated in the database
        updated_book = db.session.query(Book).get(book.id)
        assert updated_book.title == update_data['title']
        assert updated_book.author_id == update_data['author_id']
        assert updated_book.ISBN == update_data['ISBN']
        assert updated_book.publication_date == datetime.strptime(
            update_data['publication_date'], '%Y-%m-%d').date()
        assert updated_book.genre == update_data['genre']


def test_delete_book(client, auth, app):
    # create a test book
    book_data = {
        'title': 'Test Book',
        'author_id': 100,
        'ISBN': '1234567893',
        'publication_date': '2020-01-01',
        'genre': 'Test Genre1',
    }

    with app.app_context():
        # add the test book to the library
        client.post('/api/books', data=json.dumps(book_data),
                    content_type='application/json')

        # send a DELETE request to the /books/1 endpoint
        response = client.delete('/api/books/1')

        # assert that the response has a 200 status code
        assert response.status_code == 200
        # assert that the response body is {"success": True}
        assert response.json == {'success': True}

# test filter by combination of book title, author name, and available copy


def test_search_book_with_filters_and_pagination(client, auth, app):
    with app.app_context():

        authorNickname = "BBB"
        title = "AAA"
        # use pagination
        page = 1
        per_page = 10

        # send a GET request to the /api/books endpoint
        response = client.get(
            f'/api/books/search?title={title}&author=&page=1&per_page=1')

        # assert that the response has a 200 status code
        assert response.status_code == 200
        assert response.json['success'] == True
        assert len(response.json['result']) == 1


def test_search_book_with_filters(client, auth, app):
    with app.app_context():

        authorNickname = "BBB"
        title = "AAA"
        # use pagination
        page = 1
        per_page = 10

        # send a GET request to the /api/books endpoint
        response = client.get(
            f'/api/books/search?title={title}&author=&page=&per_page=')

        # assert that the response has a 200 status code
        assert response.status_code == 200
        assert response.json['success'] == True
        assert len(response.json['result']) == 2

# todo: allow override loan dates for testing the fee calculation


def test_return_copy(client, auth, app):
    with app.app_context():

        # Given
        copy = Copy(book_id=1, available=False, location="A1")
        # find 1st

        member = db.session.query(Member).first()
        # member = Member(id=1, name="John Doe")
        loan = Loan(copy=copy, member=member, loan_date=datetime.now(),
                    due_date=datetime.now() + timedelta(days=14))
        db.session.add_all([copy, member, loan])
        db.session.commit()
        assert loan.copy == copy
        assert loan.member == member
        assert loan.loan_date is not None
        assert loan.due_date is not None
        assert loan.return_date is None
        assert copy.available == False

        # When
        response = client.post(
            "/api/books/copies/{}/checkin".format(copy.id),
            content_type="application/json"
        )

        # Then
        assert response.status_code == 200
        assert response.json == {
            "success": True, 'result': 'Copy checked in successfully'}
        loan = Loan.query.first()

        assert loan.return_date is not None
        assert copy.available
      #  assert loan.fee is not None


def test_check_out_copy(client, auth, app):
    with app.app_context():
        # Given
        copy = Copy(book_id=1, available=True, location="Library A")
        memberFirst = Member(first_name="Jane", last_name="Doe",
                             email="jane1960@example.com", password="123456", is_admin=False)
        memberSecond = Member(first_name="Marry", last_name="Doe",
                              email="mary1961@example.com", password="123456", is_admin=False)
        # member = Member(id=1,  name, name="John Doe")
        db.session.add_all([copy, memberFirst, memberSecond])
        db.session.commit()

        # When
        response = client.post(
            f'/api/books/copies/{copy.id}/checkout',
            data=json.dumps({"member_id": memberFirst.id}),
            content_type="application/json"
        )

        # Then
        assert response.status_code == 200
        assert response.get_json() == {
            'success': True, 'result': "Copy checked out successfully"}
        loan = Loan.query.first()
        assert loan.copy == copy
        assert loan.member == memberFirst
        assert loan.loan_date is not None
        assert loan.due_date is not None
        assert loan.return_date is None
        assert not copy.available
        response = client.post(
            f'/api/books/copies/{copy.id}/checkout',
            data=json.dumps({"member_id": memberSecond.id}),
            content_type="application/json"
        )
        # so now copy is not available
        assert response.status_code == 400
        assert response.json == {
            'success': False, 'error': 'Copy not available'}
