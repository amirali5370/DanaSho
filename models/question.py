from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Question(db.Model):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id') ,nullable=False, index=True)
    text = Column(String, nullable=False, index=True)
    option1 = Column(String, nullable=False, index=True)
    option2 = Column(String, nullable=False, index=True)
    option3 = Column(String, nullable=False, index=True)
    option4 = Column(String, nullable=False, index=True)
    answer = Column(String, index=True)

    book = db.relationship("Book", backref=backref("questions" , lazy="dynamic"))