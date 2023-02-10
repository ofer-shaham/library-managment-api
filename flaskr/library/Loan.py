from datetime import datetime
from datetime import datetime, timedelta

from .basic import db
# from flaskr.library.Author import Author
from flaskr.library.Base import Base

# from flaskr.auth.User import User
from flaskr.library.User import User
from flaskr.library.Copy import Copy
from flaskr.library.Book import Book


from flaskr.utils.utils import convertDateStrToDateObj
from flaskr.utils.constants import LOAN_PERIOD_DAYS, FEE_DAILY_RATE


from Sqlalchemy import event


class Loan(Base):
    # __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    copy_id = db.Column(db.Integer, db.ForeignKey('copy.id'))
    # copy = relationship("Parent", back_populates="child")

    # Copy.loan = relationship("Loan", uselist=False, back_populates="copy")

    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    fee = db.Column(db.Float, nullable=False, default=0)
    return_date = db.Column(db.Date)
    # lazy="joined", back_populates="loans")

    # @staticmethod
    # def get_user_loans_count(self):
    #     result = Loan.query.filter_by(
    #         user_id=self.user_id, return_date=None).count()
    #     return result
    @staticmethod
    def get_completed_loans_fees(user):
        # get fee of completed loans only
        result = Loan.query.filter_by(
            user_id=user.id).all()
        total = 0
        for loan in result:
            total += loan.fee
        return total

    @staticmethod
    def get_active_loans_count(user):
        result = Loan.query.filter_by(
            user_id=user.id, return_date=None).count()
        return result

    @staticmethod
    def get_all_loans(user):
        # admin presented with other users' loans as well
        res = []
        queryTitles = Loan.query.join(Loan.copy).join(Copy.book).order_by(Loan.created_at).group_by(
            Loan.user_id, Book.title).with_entities(Loan.user_id, Book.title)

        if user.is_admin == False:
            queryTitles = queryTitles.filter(Loan.user_id == user.id)

        res = queryTitles.all()

        # convert to dict
        titles_dict = {}
        for title in res:
            # add to array:
            if title.user_id in titles_dict:
                titles_dict[title.user_id].append(title.title)
            else:
                titles_dict[title.user_id] = [title.title]

        return titles_dict

    @staticmethod
    def create_loan(copy, user, loan_date=None, due_date=None):
        # assumes that the copy is available

        loan = Loan(copy=copy, user=user)
        loan.copy = copy
        loan.user = user

        if loan_date is None:
            loan.loan_date = datetime.now()
        else:
            loan.loan_date = loan_date
        if due_date is None:
            loan.due_date = loan.loan_date + timedelta(days=LOAN_PERIOD_DAYS)
        else:
            loan.due_date = due_date

        copy.available = False
        return loan

    @staticmethod
    def return_loan(copy):

        loan = Loan.query.filter_by(copy_id=copy.id).first()
        loan.return_date = datetime.now()
        copy = db.session.get(Copy, copy.id)
        copy.available = True
        copy.loan = None
        loan.update_loan_fee()

    def update_loan_fee(self):
        if (self.return_date):
            datetime1 = datetime(
                self.due_date.year, self.due_date.month, self.due_date.day)

            if (self.return_date.date() > self.due_date):
                self.fee = (self.return_date -
                            datetime1).days * FEE_DAILY_RATE
            else:
                self.fee = 0

    def to_dict(self):
        return {
            'id': self.id,
            'copy_id': self.copy_id,
            'user_id': self.user_id,
            'loan_date': self.loan_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'user': self.user.to_dict(),
            'copy': self.copy.to_dict()
        }


@event.listens_for(Loan, 'before_insert')
@event.listens_for(Loan, 'before_update')
def pre_create_update_hook(mapper, connection, target):
    if (target.return_date):
        target.return_date = convertDateStrToDateObj(
            connection.engine, target.return_date)
