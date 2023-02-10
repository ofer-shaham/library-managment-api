
# from datetime import datetime
from flaskr.library.basic import db
from flaskr.library.Base import Base
# from sqlalchemy import event


class Copy(Base):
    # __tablename__ = 'copies'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False, default='general')
    available = db.Column(db.Boolean, default=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"))
    # loan_id = db.Column(db.Integer, db.ForeignKey("loan.id"))

    # def __init__(self, book_id,  location='general'):
    #     self.location = location
    #     self.book_id = book_id

    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'book_id': self.book_id,
            'loan_id': self.loan.id,
            'available': self.available,
            # 'loan': self.loan.to_dict() if self.loan else None
        }

    def isAvailable(self):
        """Check if any copies of this book are available for loan."""
        return self.available
