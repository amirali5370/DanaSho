from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Book(db.Model):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    about = Column(String, nullable=False, index=True)
    grade = Column(Integer, nullable=False, index=True)
    primalink = Column(String, nullable=False, index=True)

    time = Column(Integer, index=True)
    number = Column(Integer, index=True ,default=0)