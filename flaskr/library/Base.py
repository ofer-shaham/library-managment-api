from datetime import datetime
from datetime import timezone

from flaskr import db


from sqlalchemy.ext.declarative import declared_attr


def now_utc():
    return datetime.now(timezone.utc)


class Base(db.Model):
    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
