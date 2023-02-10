from flask_sqlalchemy import SQLAlchemy

from flask import Flask
# from flaskr import generateData, create_app


db = SQLAlchemy()


class Author(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


class Book(Base):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey(
        "author.id"), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,

        }


class Copy(Base):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    # loan_id = db.Column(db.Integer, db.ForeignKey("loan.id"), nullable=True)


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)


class Loan(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    copy_id = db.Column(db.Integer, db.ForeignKey("copy.id"), nullable=False)


class Post(Base):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)


Author.books = db.relationship("Book", back_populates="author")
Book.author = db.relationship("Author", back_populates="books")
Book.copies = db.relationship("Copy", back_populates="book")
Copy.book = db.relationship("Book", back_populates="copies")
Copy.loan = db.relationship("Loan", back_populates="copy")
User.loans = db.relationship("Loan", back_populates="user")
User.posts = db.relationship("Post", back_populates="user")
Loan.user = db.relationship("User", back_populates="loans")
Loan.copy = db.relationship("Copy", back_populates="loan")
Post.user = db.relationship("User", back_populates="posts")


def generateData():
    author1 = Author(name="Author One")
    author2 = Author(name="Author Two")
    book1 = Book(title="Book One", author=author1)
    book2 = Book(title="Book Two", author=author1)
    book3 = Book(title="Book Three", author=author2)
    copy1 = Copy(book=book1)
    copy2 = Copy(book=book1)
    copy3 = Copy(book=book2)
    copy4 = Copy(book=book3)
    user1 = User(name="User One")
    user2 = User(name="User Two")
    loan1 = Loan(user=user1, copy=copy1)
    loan2 = Loan(user=user1, copy=copy2)
    loan3 = Loan(user=user2, copy=copy3)
    post1 = Post(user=user1, content="Sample Content")
    post2 = Post(user=user2, content="Sample Content")

    return [author1, author2, book1, book2, book3, copy1, copy2, copy3, copy4, user1, user2, loan1, loan2, loan3, post1, post2]


def create_app(test_config=None):
    # app = Flask(__name__, instance_relative_config=True)
    app = Flask(__name__)  # , instance_relative_config=True)
    # app.cli.add_command(init_db_command)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)
    if __name__ == "__main__":
        # replace with your database connection string
        # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
        db.init_app(app)

        # app = create_app(
        #     {"TESTING": True, "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"})

        # # create the database and load test data
        # # set _password to pre-generated hashes, since hashing for each test is slow

    return app


def init_db():
    db.drop_all()
    db.create_all()


def test():
    # setup test config
    file = 'sqlite:////tmp/test.db'
    memory = "sqlite:///:memory:"
    app = create_app(
        {"TESTING": True, "SQLALCHEMY_DATABASE_URI": file})

    # create the database and load test data
    # set _password to pre-generated hashes, since hashing for each test is slow

    with app.app_context():
        init_db()
        # user = User(name="test")

        data = generateData()
        print(data)
        # save data to db
        db.session.add_all
        (
            # generate data
            data
        )
        result = db.session.commit()
        print(result)
        # db.session.close()
        # db.session()
        # Return a list of all books
        book = db.session.query(Book).first()
        if book:
            book.to_dict()
        else:
            print("No book found")
        books = db.session.query(Book).all()
        # return jsonify([book.to_dict() for book in books])
        if books:
            dicted = ([book.to_dict() for book in books])
            print(dicted)
        else:
            print("No books found")

        # print(jsonify({'success': True, 'result': dicted}))


test()
# @click.command("init-db")
# @with_appcontext
# def init_db_command():
#     """Clear existing data and create new tables."""
#     init_db()
#     click.echo("Initialized the database.")
