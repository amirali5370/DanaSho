from sqlalchemy import *
from extentions import db

class Slide(db.Model):
    __tablename__ = "slides"
    id = Column(Integer, primary_key=True)
    head = Column(String, nullable=False, index=True)
    text = Column(String, nullable=False, index=True)
    active = Column(Integer, nullable=False, index=True)