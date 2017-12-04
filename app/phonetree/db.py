# -*- coding: utf-8 -*-
import os
from . import db


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    db.drop_all()
    db.create_all()

    db.session.commit()
