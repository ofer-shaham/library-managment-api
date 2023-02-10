
from flaskr.library.Loan import Loan
from flaskr.library.User import User
from flaskr.library.Copy import Copy
from flaskr.library.Book import Book
from flaskr.library.Author import Author
from flaskr.library.Post import Post

from .basic import db

Author.books = db.relationship("Book", back_populates="author")
Book.author = db.relationship("Author", back_populates="books")
Book.copies = db.relationship("Copy", back_populates="book")
Copy.book = db.relationship("Book", back_populates="copies")
# Copy.loan = db.relationship("Loan", back_populates="copy")
User.loans = db.relationship("Loan", back_populates="user")
User.posts = db.relationship("Post", back_populates="user")
Loan.user = db.relationship("User", back_populates="loans")
Loan.copy = db.relationship("Copy", back_populates="loan")
Post.user = db.relationship("User", back_populates="posts")
Copy.loan = db.relationship("Loan", uselist=False, back_populates="copy")

# Base = declarative_base()

# # from .parent import Parent
# # from .child import Child

# # import Loan:


# # Add the relationship after both classes have been defined
# User.loans = db.relationship("Loan", back_populates="user")
# User.posts = db.relationship("Post", back_populates="user")

# Author.books = db.relationship(
#     "Book", back_populates="author")

# Book.copies = db.relationship(
#     "Copy", back_populates="book")


# # Loan.user = db.relationship("User", back_populates="loans")
# Post.user = db.relationship("User", back_populates="posts")
# Book.author = db.relationship(
#     "Author", back_populates="books", foreign_keys=Book.author_id)
# Copy.book = db.relationship(
#     "Book", back_populates="copies", foreign_keys=Copy.book_id)
# Loan.copy = db.relationship(
#     "Copy", back_populates="loan", foreign_keys=Loan.copy_id)
# Copy.loan = db.relationship(
#     "Loan", back_populates="copy")
# Loan.user = db.relationship(
#     "User", back_populates="loans", foreign_keys=Loan.user_id)

# Loan
# copy = db.relationship('Copy', back_populates="loan")
# # user = db.relationship('User', back_populates="loan")
# user = db.relationship('User', lazy="joined", back_populates="loans")
# author = db.relationship(
# "Author", back_populates="books", foreign_keys=[author_id])
# copies = db.relationship("Copy", back_populates="book")
# posts = db.relationship('Post', back_populates="user")
# loans = db.relationship('Loan', back_populates="user")

# user = db.relationship(User,  # lazy="joined",
#                        back_populates="posts", foreign_keys=[user_id])

# book = db.relationship(
#     "Book", back_populates="copies", foreign_keys=[book_id])
# loan = db.relationship('Loan', uselist=False, back_populates="copy")
