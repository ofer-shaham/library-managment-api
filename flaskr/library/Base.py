from datetime import datetime
from datetime import timezone

from flaskr.library.basic import db


from sqlalchemy.ext.declarative import declared_attr
# from sqlalchemy.orm import declarative_base


def now_utc():
    return datetime.now(timezone.utc)
# db.Model


# Base0 = declarative_base()


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
