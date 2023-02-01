from datetime import datetime
from datetime import datetime, timedelta

from flaskr import db
from flaskr.library.Author import Author
from flaskr.library.Base import Base
from flaskr.library.Member import Member
from flaskr.library.Copy import Copy
from flaskr.utils.utils import convertDateStrToDateObj
from flaskr.utils.constants import LOAN_PERIOD_DAYS, FEE_DAILY_RATE


from sqlalchemy import event


class Loan(Base):
    __tablename__ = 'loans'

    id = db.Column(db.Integer, primary_key=True)
    copy_id = db.Column(db.Integer, db.ForeignKey(Copy.id))
    member_id = db.Column(db.ForeignKey(Member.id), nullable=False)
    loan_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    fee = db.Column(db.Float, nullable=False, default=0)
    return_date = db.Column(db.Date)
    member = db.relationship(Member, lazy="joined", back_populates="loans")
    copy = db.relationship('Copy', back_populates="loan")

    @staticmethod
    def create_loan(copy, member):
        loan = Loan(copy=copy, member=member)
        loan.copy = copy
        loan.member = member

        loan.loan_date = datetime.now()
        loan.due_date = loan.loan_date + timedelta(days=LOAN_PERIOD_DAYS)
        copy.available = False
        return loan

    @staticmethod
    def return_loan(copy):

        loan = Loan.query.filter_by(copy_id=copy.id).first()
        loan.return_date = datetime.now()
        copy = Copy.query.get(copy.id)
        copy.available = True
        loan.copy.loan = None
        loan.calculate_fee()

    def calculate_fee(self):
        if (self.return_date):
            if (self.return_date.date() > self.due_date):
                self.fee = (self.return_date -
                            self.due_date).days * FEE_DAILY_RATE
            else:
                self.fee = 0

    def to_dict(self):
        return {
            'id': self.id,
            'copy_id': self.copy_id,
            'member_id': self.member_id,
            'loan_date': self.loan_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'member': self.member.to_dict(),
            'copy': self.copy.to_dict()
        }


@event.listens_for(Loan, 'before_insert')
@event.listens_for(Loan, 'before_update')
def pre_create_update_hook(mapper, connection, target):
    if (target.return_date):
        target.return_date = convertDateStrToDateObj(
            connection.engine, target.return_date)
