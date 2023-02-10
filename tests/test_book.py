from datetime import datetime, timedelta
import json
import pytest

from flaskr.utils.constants import dateFormatFromServer
from flaskr.utils.constants import dateFormarToServer
from flaskr.utils.utils import convertTimeToEpocSeconds
# from  flaskr.library.basic import db


from flaskr import init_db, create_app
# from flaskr.auth.User import User
from flaskr.library.Copy import Copy
from flaskr.library.Book import Book
from flaskr.library.Loan import Loan
from flaskr.library.User import User
from flaskr.library.Author import Author

from flask import g

from flask import session
from flaskr.library.models import db
# TODO: add userSession class to store user session data


credentials1 = {'username': 'user1', 'password': 'user1'}


class Helpers:
    @ staticmethod
    def userCheckout(client, copy_id):

        response = client.post(
            f'/api/books/copies/{copy_id}/checkin',
            content_type="application/json"
        )
        return response


def create_book_data():
    book_data = {
        'title': 'Test Book',
        # 'author_id': 100,
        'ISBN': '1234567896',
        'publication_date': '2020-01-01',
        'genre': 'Test Genre1',
    }
# override with random ISBN
    book_data['ISBN'] = str(datetime.now())
    return book_data


@pytest.fixture
def app():
    from flaskr.library.User import User
    """Create and configure a new app instance for each test."""
    # create the app with common test config
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

    with app.app_context():
        init_db()

        # for admin

        user1 = User(username="user1", password="user1", is_admin=False)
        user2 = User(username="user2", password="user2", is_admin=False)
        adminUser = User(username="admin", password="admin", is_admin=True)

        author = Author(nickname="John Smith1",
                        first_name="John", last_name="Smith")
        book = Book(title="My Book", author=author, ISBN="1234567892",
                    publication_date='2000-11-11', genre="Test Genre1")

        book1 = Book(title='Test Book1 AAAA', author=author, ISBN='1234567894',
                     publication_date='2020-01-01', genre='Test Genre1')

        book2 = Book(title='Test Book2', author=author, ISBN='1234567890',
                     publication_date='2020-01-01', genre='Test Genre1')

        book3 = Book(title='Test Book1 AAA', author=author, ISBN='1234567895',
                     publication_date='2020-01-01', genre='Test Genre1')

        db.session.add_all(
            [book, book1, book2, book3,  user1, user2, adminUser])

        db.session.commit()

    yield app


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("admin", "admin", True, 200),
        ("user1", "user1", False, 401),
        ("user2", "user2", False, 401),

    ),
)
# todo: - should not be able to change: author_id
def test_update_book(client, auth, app, username, password, is_admin, status_code):
    # create a new book
    book_id = 2
    with app.app_context():
        # login user
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:

            update_data = {
                'title': 'Updated Test Book' + str(datetime.now()),

            }

            # send a PUT request to the /api/books/<book_id> endpoint
            response = client.put(
                f'/api/books/{book_id}', data=json.dumps(update_data), content_type='application/json')

            # assert that the response has a 201 status code on success
            assert response.status_code == status_code
            if (status_code == 200):
                assert response.json['success'] == True
                assert response.json['result']['id'] > 0
                assert response.json['result']['created_at'] is not None
                assert response.json['result']['updated_at'] is not None
            else:
                assert response.json['success'] == False
                assert response.json['error'] == 'Unauthorized'


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("admin", "admin", True, 201),
        ("user1", "user1", False, 401),
        ("user2", "user2", False, 401),

    ),
)
def test_add_book(client, auth, app, username, password, is_admin, status_code):

    with app.app_context():
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:
            book_data = create_book_data()
            data = json.dumps(book_data)
            response = client.post(
                '/api/books', data=data, content_type='application/json')
            # assert that the response has a 201 status code on success
            assert response.status_code == status_code
            if (status_code == 201):
                assert response.json['success'] == True
                assert response.json['result']['id'] > 0
                assert response.json['result']['created_at'] is not None
                assert response.json['result']['updated_at'] is not None
            else:
                assert response.json['success'] == False
                assert response.json['error'] == 'Unauthorized'


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("user1", "user1", False, 401),
        ("user2", "user2", False, 401),
        ("admin", "admin", True, 200),

    ),
)
def test_add_book(client, auth, app, username, password, is_admin, status_code):
    # create a new book
    book_id = 1
    with app.app_context():
        # login user
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:
            # assert session['user_id'] is not None
            book_data = create_book_data()
            data = json.dumps(book_data)
            response = client.delete('/api/books/{}'.format(book_id))

            # assert that the response has a 201 status code on success
            assert response.status_code == status_code


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("user1", "user1", False, 200),
        ("user2", "user2", False, 200),
        ("admin", "admin", True, 200),
    )
)
def test_get_books(client, auth, app, username, password, is_admin, status_code):
    with app.app_context():
        book = db.session.query(Book).first()
        response = client.get('/api/books')

        # assert that the response has a 200 status code
        assert response.status_code == 302
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:
            # send a GET request to the /api/books endpoint
            response = client.get('/api/books')

            # assert that the response has a 200 status code
            assert response.status_code == 200
            assert response.json['success'] == True

            # assert that the response contains the test book
            assert response.json['result'][0]['title'] == book.to_dict()[
                'title']


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("user1", "user1", False, 401),
        ("user2", "user2", False, 401),
        ("admin", "admin", True, 200),
    )
)
def test_get_book(client, auth, app, username, password, is_admin, status_code):
    with app.app_context():
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:
            book = db.session.query(Book).first()
            # db.session.commit()

            # send a GET request to the /api/books/<book_id> endpoint
            response = client.get(f'/api/books/{book.id}')

            # assert that the response has a 200 status code
            assert response.status_code == 200
            assert response.json['success'] == True

            # assert that the response contains the test book
            assert response.json['result']['id'] == 1
            assert response.json['result']['ISBN'] == '1234567892'


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("admin", "admin", True, 200),
        ("user1", "user1", False, 401),
        ("user2", "user2", False, 401),

    ),
)
def test_delete_book(client, auth, app, username, password, is_admin, status_code):
    # create a test book
    book_id = 1
    response = auth.login(username, password)
    assert response.status_code == 302
    with app.app_context():
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:
            response = client.delete('/api/books/{}'.format(book_id))

            assert response.status_code == status_code

            if (status_code == 200):
                assert response.json['result']['id'] == book_id
            else:
                assert response.json['success'] == False
                assert response.json['error'] == 'Unauthorized'


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("user1", "user1", False, 200),
        ("user2", "user2", False, 200),
        ("admin", "admin", True, 200),
    )
)
def test_search_book_with_filters_and_pagination(client, auth, app,
                                                 username, password, is_admin, status_code):
    # test filter by combination of book title, author name, and available copy

    with app.app_context():
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:
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


@ pytest.mark.parametrize(
    ("username", "password", "is_admin", "status_code"),
    (
        ("user1", "user1", False, 200),
        ("user2", "user2", False, 200),
        ("admin", "admin", True, 200),
    )
)
def test_search_book_with_filters(client, auth, app,
                                  username, password, is_admin, status_code):
    with app.app_context():
        response = auth.login(username, password)
        assert response.status_code == 302
        with client:
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


def test_return_copy(client, auth, app):

    # schenario:
    # user1 and user2 takes a loan

    with app.app_context():
        credentials2 = {'username': 'user2', 'password': 'user2'}

        # use existing users and book
        book1 = db.session.get(Book, 1)

        user1 = db.session.get(User, 1)
        user2 = db.session.get(User, 2)

        # create copies
        copy1 = Copy(book=book1)
        copy2 = Copy(book=book1)

        # create loans
        loan1 = Loan.create_loan(copy1, user1)
        loan2 = Loan.create_loan(copy2, user2)
        db.session.add_all([copy1, copy2, loan1, loan2])
        db.session.commit()

        response = auth.login(
            credentials1['username'], credentials1['password'])

        assert response.status_code == 302

        with client:
            assert copy1.loan.user_id == user1.id

            response = Helpers.userCheckout(client,
                                            copy1.id)
            assert response.status_code == 200
            response = Helpers.userCheckout(client,
                                            copy2.id)
            # user1 can return his loaned copy
            assert response.status_code == 401
            response = Helpers.userCheckout(client,
                                            copy1.id)
            # copy is available, can't return again
            assert response.status_code == 400
            response = Helpers.userCheckout(client,
                                            0)
            assert response.status_code == 404


def test_check_out_copy(client, auth, app, monkeypatch):

    with app.app_context():
        book_id = 1
        copy = Copy(book_id=book_id, location="Library A")

        # no copies available
        assert db.session.query(Copy).count() == 0

        db.session.add_all([copy])
        db.session.commit()

        # there is 1 available copy
        assert db.session.query(Copy).first().available == True

        response = response = auth.login(
            credentials1['username'], credentials1['password'])

        assert response.status_code == 302

        with client:
            monkeypatch.setattr("flaskr.utils.constants.MAX_CHECKED_OUT", 0)
            # user checks out a copy
            response = client.post(
                f'/api/books/copies/{copy.id}/checkout',
                content_type="application/json"
            )

            # Then
            assert response.json == {
                'error': 'User has reached limit of 0 checked out book copies', 'success': False}
            assert response.status_code == 400
            assert response.json['success'] == False

            # allow max of 2 active loans for user
            monkeypatch.setattr("flaskr.utils.constants.MAX_CHECKED_OUT", 2)
            response = client.post(
                f'/api/books/copies/{copy.id}/checkout',
                content_type="application/json"
            )

            assert response.status_code == 200
            assert response.json['success'] == True
            loan = response.json['result']
            assert loan['copy'] == copy.to_dict()
            assert loan['user_id'] == session['user_id']
            assert loan['loan_date'] is not None
            assert loan['due_date'] is not None
            assert loan['return_date'] is None
            assert not copy.available

            # the copy is no longer available
            response = client.post(
                f'/api/books/copies/{copy.id}/checkout',
                content_type="application/json"
            )
            # so now copy is no longer available
            assert response.status_code == 400
            assert response.json == {
                'success': False, 'error': 'Copy is not available'}


@pytest.fixture
def loan_history_context(app):
    with app.app_context():
        copy1 = Copy(book_id=1)
        copy2 = Copy(book_id=1)
        copy3 = Copy(book_id=2)

        user1 = db.session.get(User, 1)
        user2 = db.session.get(User, 2)

        loan1 = Loan.create_loan(copy1, user1)
        loan2 = Loan.create_loan(copy2, user1)
        loan3 = Loan.create_loan(copy3, user1)

        loan1user2 = Loan.create_loan(copy1, user2)

        db.session.add_all([copy1, copy2, copy3, user1,
                           loan1, loan2, loan3, loan1user2])
        db.session.commit()
        yield app


@pytest.fixture
def loan_history_with_fee_context(app):
    with app.app_context():
        copy1 = Copy(book_id=1)
        copy2 = Copy(book_id=1)
        copy3 = Copy(book_id=2)

        user1 = db.session.get(User, 1)

        loan1 = Loan.create_loan(copy1, user1,  datetime.now(
        ) - timedelta(days=20),  datetime.now() - timedelta(days=10))
        loan2 = Loan.create_loan(copy2, user1,  datetime.now(
        ) - timedelta(days=20),  datetime.now() - timedelta(days=10))
        loan3 = Loan.create_loan(copy3, user1)

        db.session.add_all([copy1, copy2, copy3, user1,
                           loan1, loan2, loan3])
        db.session.commit()
        Loan.return_loan(loan1.copy)
        Loan.return_loan(loan2.copy)
        db.session.commit()

        yield app


@ pytest.mark.parametrize(


    ("username", "password", "book_titles"),
    (("user2", "user2", {'2': ['My Book']}),
     ("user1", "user1",    {'1': ['My Book', 'Test Book1 AAAA']}),
     ("admin", "admin",   {'1': ['My Book', 'Test Book1 AAAA'], '2': ['My Book']}))
)
def test_loans(client, auth, loan_history_context, username, password, book_titles):
    # user 1 has 2 books checked out
    # user 1 has 2 books checkout out
    # book 1: checked out

    with loan_history_context.app_context():

        response = auth.login(
            username, password)
        assert response.status_code == 302
        with client:
            response = client.get(
                "/api/books/checked-out-history/all",
                content_type="application/json"
            )
            assert response.status_code == 200
            assert response.json == {
                "success": True, 'result': {'user_loans': book_titles}}


def test_loans_fee(client, auth, loan_history_with_fee_context):

    with loan_history_with_fee_context.app_context():

        response = auth.login(
            'user1', 'user1')
        assert response.status_code == 302

        with client:
            response = client.get(
                "/api/books/checked-out-history/fees",
                content_type="application/json"
            )
            assert response.status_code == 200
            assert response.json == {
                "success": True, 'result': {'fees': 2.0}}


def test_onUpdate_trim_string_on_input_validation(client, auth, app):

    book_id = 2
    book_data_with_spaces = {
        'title': '  Test Book   ',
        'author_id': 100,
        'ISBN': '  1234567896  ',
        'publication_date': '  2020-01-11  ',
        'genre': '  Test Genre1  ',
    }
    book_data_expected = {
        'title': 'Test Book',
        'author_id': 100,
        'ISBN': '1234567896',
        'publication_date': '2020-01-11',
        'genre': 'Test Genre1',
    }
    with app.app_context():
        # login user
        response = auth.login('admin', 'admin')
        assert response.status_code == 302
        with client:
            # update the title of the book
            response = client.put(
                f'/api/books/{book_id}',
                data=json.dumps(book_data_with_spaces),
                content_type="application/json"
            )
            assert response.status_code == 200
            assert response.json['success'] == True
            assert response.json['result']['ISBN'] == book_data_expected['ISBN']
            assert response.json['result']['title'] == book_data_expected['title']
            assert response.json['result']['genre'] == book_data_expected['genre']

            assert convertTimeToEpocSeconds(response.json['result']['publication_date'], dateFormatFromServer) == convertTimeToEpocSeconds(
                book_data_expected['publication_date'], dateFormarToServer)


def test_onCreate_trim_string_on_input_validation(client, auth, app):

    book_id = 2
    with app.app_context():
        # login user
        book_data_expected = {
            'title': 'Test Book',
            'author_id': 100,
            'ISBN': '1234567896',
            'publication_date': '2020-01-11',
            'genre': 'Test Genre1',
        }
        book_data_with_spaces = {
            'title': '  Test Book   ',
            'author_id': 100,
            'ISBN': '  1234567896  ',
            'publication_date': '  2020-01-11  ',
            'genre': '  Test Genre1  ',
        }
        response = auth.login('admin', 'admin')
        assert response.status_code == 302
        with client:
            data = json.dumps(book_data_with_spaces)
            response = client.post(
                '/api/books', data=data, content_type='application/json')
            # update the title of the book

            assert response.status_code == 201
            assert response.json['success'] == True
            assert response.json['result']['ISBN'] == book_data_expected['ISBN']
            assert response.json['result']['title'] == book_data_expected['title']
            assert response.json['result']['genre'] == book_data_expected['genre']

            assert convertTimeToEpocSeconds(response.json['result']['publication_date'], dateFormatFromServer) == convertTimeToEpocSeconds(
                book_data_expected['publication_date'], dateFormarToServer)
