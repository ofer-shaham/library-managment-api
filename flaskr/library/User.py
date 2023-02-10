from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.library.basic import db
# import Loan:
# import Loan
# from flaskr.library.Loan import Loan


from flaskr.library.Base import Base

from .basic import db


class User(Base):

    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)

    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(255))
    # password = db.Column(db.String(255), nullable=False)
    # Unique constraint on email
    # __table_args__ = (db.UniqueConstraint('email'),)
    # relationship
#

    def set_password(self, value):
        """Store the password as a hash for security."""
        self.password_hash = generate_password_hash(value)

    password = property(fset=set_password)
    # allow password = "..." to set a password

    # def __init__(self, username, password, is_admin) -> None:
    #     super().__init__()
    #     self.username = username
    #     self.set_password(password)
    #     self.is_admin = is_admin

    def check_password(self, value):
        return check_password_hash(self.password_hash, value)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            # 'password': self.password,
            'is_admin': self.is_admin,
        }
