from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from flaskr.library.Base import Base
from flaskr import db


class Author(Base):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    nickname = db.Column(db.String, nullable=False)

    # relationship
    books = db.relationship("Book", back_populates="author")

    # to_dict
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'nickname': self.nickname,
            'updated_at': self.updated_at,
            'created_at': self.created_at,
        }
