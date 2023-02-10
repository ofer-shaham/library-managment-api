from datetime import datetime
from datetime import timezone

from flask import url_for

from flaskr.library.basic import db
from flaskr.library.Base import Base
from flaskr.library.User import User


def now_utc():
    return datetime.now(timezone.utc)


class Post(Base):
    # __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('user.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=now_utc)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)

    @property
    def update_url(self):
        return url_for("blog.update", id=self.id)

    @property
    def delete_url(self):
        return url_for("blog.delete", id=self.id)
