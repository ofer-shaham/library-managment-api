from datetime import datetime
from datetime import timezone

from flaskr import db
from flaskr.library.Author import Author

from sqlalchemy import event

from sqlalchemy.ext.declarative import declared_attr

from flaskr.library.Base import Base


# todo: add properties: phone, address
class Member(Base):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    # Unique constraint on email
    __table_args__ = (db.UniqueConstraint('email'),)
    # relationship
    loans = db.relationship("Loan", back_populates="member")

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            'is_admin': self.is_admin,
        }
