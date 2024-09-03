from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Book(db.Model):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    about = Column(String, nullable=False, index=True)
    grade = Column(String, nullable=False, index=True)