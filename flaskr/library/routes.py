
# from flaskr.library.Book import Book
from datetime import datetime, timedelta
from flask import Blueprint
from flask import jsonify, request
from flaskr.library.models import db

from flask import Flask, request, jsonify
from flaskr.library.Book import Book
from flaskr.library.Loan import Loan

# from flaskr.library.Copy import Copy
# from flaskr.library.Loan import Loan
from flask import g

# from flask import session
from flaskr.auth.views import login_required
from flaskr.library.Copy import Copy
from flaskr.library.Loan import Loan

from flaskr.library.User import User

app = Flask(__name__)
bpBooks = Blueprint("book", __name__, url_prefix="/api")


@bpBooks.route('/books', methods=['GET', 'POST'])
@login_required
def books():
    # import Book:

    if request.method == 'GET':
        # Return a list of all books
        books = db.session.query(Book).all()
        # return jsonify([book.to_dict() for book in books])
        dicted = ([book.to_dict() for book in books])
        return jsonify({'success': True, 'result': dicted}), 200

    elif request.method == 'POST':
        # authorization
        if (g.user.is_admin == False):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        # Add a new book to the library
        data = request.get_json()
        for key, value in data.items():
            data[key] = value.strip() if isinstance(value, str) else value

        new_book = Book(title=data['title'], author_id=data['author_id'], ISBN=data['ISBN'],
                        publication_date=data['publication_date'], genre=data['genre'])
        db.session.add(new_book)
        db.session.commit()
        return jsonify({'success': True, 'result': new_book.to_dict()}), 201


@bpBooks.route('/books/<int:book_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def book(book_id):
    from flaskr.library.Book import Book
    book = db.session.get(Book, book_id)
    if request.method == 'GET':
        # Return a single book
        return jsonify({'success': True, 'result': book.to_dict()})
    elif request.method == 'PUT':
        if (g.user.is_admin == False):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        # Update an existing book
        # update only if property is present in the request
        data = request.get_json()
        for key, value in data.items():
            data[key] = value.strip() if isinstance(value, str) else value

        if 'title' in data:
            book.title = data['title']
        if 'author_id' in data:
            book.author_id = data['author_id']
        if 'ISBN' in data:
            book.ISBN = data['ISBN']
        if 'publication_date' in data:
            book.publication_date = data['publication_date']
        if 'genre' in data:
            book.genre = data['genre']
        db.session.commit()

        return jsonify({'success': True, 'result': book.to_dict()}), 200

    if request.method == 'DELETE':
        if (g.user.is_admin == False):
            return jsonify({'success': False, 'error': 'Unauthorized'}), 401
        # Delete an existing book
        db.session.delete(book)
        db.session.commit()
        return jsonify({'success': True, 'result': {'id': book_id}}), 200


@bpBooks.route('/books/search', methods=['GET'])
@login_required
def search_books():
    from flaskr.library.Book import Book
    """Search for books by title and/or author and available copies"""
    """available is set to 1 if the user wants to search for available books only"""
    books = []

    title = request.args.get('title')
    authorNickname = request.args.get('author')
    # cast to boolean to match the model type
    available = request.args.get('available') == '1'
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    query = None

    # if parameter is not set, or it's empty convert to None or set default value
    if title == '':
        title = None
    if authorNickname == '':
        authorNickname = None
    if available == '':
        available = None
    if page == '':
        page = 1
    if per_page == '':
        per_page = 10

    if (title is None and authorNickname is None and available is None):
        # no filters
        query = db.session.query(Book)
    else:
        query = Book.search(title=title, authorNickname=authorNickname,
                            available=available)

    pagination = query.paginate(page=page, per_page=per_page)
    books = pagination.items
    # if items not found, return empty list

    dicted = ([book.to_dict() for book in books])
    return jsonify({'success': True, 'result': dicted}), 200


@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'


@ bpBooks.route('/books/checked-out-history/<filter_name>', methods=['GET'])
@login_required
def query_user_loan_history(filter_name):

    # get user's loans history (checked out books)
    # filter_name: 'all', 'active', 'fees'
    res = []
    if filter_name == 'all':
        res = {'user_loans': Loan.get_all_loans(g.user)}
    # todo: uncomment to activate option
    # elif filter_name == 'active':
    #     res = Loan.get_active_loans_count(g.user)
    elif filter_name == 'fees':
        res = {'fees': Loan.get_completed_loans_fees(g.user)}

    return jsonify({'success': True, 'result': res}), 200


@ bpBooks.route("/books/copies/<int:copy_id>/checkout", methods=["POST"])
@login_required
def check_out_copy(copy_id):
    from flaskr.utils.constants import MAX_CHECKED_OUT

    user = g.user
    if user is None:
        return jsonify({'success': False, "error": "User is not found"}), 404
    copy = db.session.get(Copy, copy_id)
    if copy is None:
        return jsonify({'success': False, "error": "Copy is not found"}), 404
    if not copy.isAvailable():
        return jsonify({'success': False, "error": "Copy is not available"}), 400


# verify user has less than <MAX_CHECKED_OUT> books checked out
    if Loan.get_active_loans_count(g.user) >= MAX_CHECKED_OUT:
        return jsonify({'success': False, "error": "User has reached limit of {} checked out book copies".format(MAX_CHECKED_OUT)}), 400

    loan = Loan.create_loan(copy, user)
    db.session.add(loan)
    db.session.commit()
    return jsonify({'success': True, 'result': loan.to_dict()}), 200


@bpBooks.route("/books/copies/<int:copy_id>/checkin", methods=["POST"])
@login_required
def check_in_copy(copy_id):
    # from flaskr.library.Loan import Loan
    # from flaskr.library.Copy import Copy

    copy = db.session.get(Copy, copy_id)

    if copy is None:
        return jsonify({'success': False, "error": "Copy not found"}), 404
    if copy.isAvailable():
        return jsonify({'success': False, "error": "Copy is not available"}), 400
    if g.user.id == copy.loan.user_id:
        Loan.return_loan(copy)
        db.session.commit()
        return jsonify({"success": True, 'result': "Copy checked in successfully"}), 200
    else:
        return jsonify({'success': False, "error": "Copy not checked out by user"}), 401
