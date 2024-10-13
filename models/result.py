from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Result(db.Model):
    __tablename__ = "results"
    id = Column(Integer, primary_key=True)
    enter = Column(Integer, nullable=False, default=1, index=True)
    user_id = Column(Integer, ForeignKey('users.id') ,nullable=False, index=True)
    book_id = Column(Integer, ForeignKey('books.id') ,nullable=False, index=True)
    score = Column(Integer, index=True)

    user = db.relationship("User", backref=backref("results" , lazy="dynamic"))
    book = db.relationship("Book", backref=backref("results" , lazy="dynamic"))