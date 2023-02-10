from datetime import datetime

from flaskr.library.basic import db
from flaskr.library.Author import Author
from flaskr.library.Base import Base
from flaskr.library.Copy import Copy
from sqlalchemy import and_
from sqlalchemy import event
from flaskr.utils.utils import convertDateStrToDateObj


class Book(Base):
    # __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)

    ISBN = db.Column(db.String(13), unique=True, nullable=True)
    publication_date = db.Column(db.Date)
    genre = db.Column(db.String(255))

    author_id = db.Column(db.Integer, db.ForeignKey(
        "author.id"), nullable=False)

    @staticmethod
    def search(title=None, authorNickname=None, available=None):
        cls = Book
        query = cls.query

        # Filter by title
        if title:
            query = query.filter(Book.title.like(f'%{title}%'))

        # Filter by author nickname
        if authorNickname:
            query = query.join(Author).filter(
                Author.nickname.like(f'%{authorNickname}%'))

        # Filter by availability
        if available:
            query = query.join(Copy).filter(Copy.available == True)

        # return query
        return query

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'ISBN': self.ISBN,
            'publication_date': self.publication_date,
            'genre': self.genre,
            'author': self.author.to_dict() if self.author else None,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
        }


@event.listens_for(Book, 'before_insert')
@event.listens_for(Book, 'before_update')
def pre_create_update_hook(mapper, connection, target):
    if (target.publication_date):
        target.publication_date = convertDateStrToDateObj(
            connection.engine, target.publication_date)
