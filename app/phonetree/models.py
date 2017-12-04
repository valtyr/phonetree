import uuid
from datetime import datetime

from phonetree import db


class Recording(db.Model):
    __tablename__ = 'phone'
    id = db.Column(db.Integer, primary_key=True)
    added_on = db.Column(db.DateTime, default=datetime.now)
    url = db.Column(db.String())
    caller = db.Column(db.String())
