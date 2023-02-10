
# from datetime import datetime
from sqlalchemy import ForeignKey
from flaskr import db
from flaskr.library.Base import Base
# from sqlalchemy import event


class Copy(Base):
    __tablename__ = 'copies'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)
    loan = db.relationship('Loan', uselist=False, back_populates="copy")
    available = db.Column(db.Boolean, default=True)
    book_id = db.Column(db.Integer, ForeignKey("books.id"))
    book = db.relationship(
        "Book", back_populates="copies", foreign_keys=[book_id])

    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'status': self.status,
            'loan': self.loan.to_dict() if self.loan else None
        }

    def isAvailable(self):
        """Check if any copies of this book are available for loan."""
        return self.available
