from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Interaction(db.Model):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True, default="review")
    content = Column(String, nullable=False, index=True)
    book_id = Column(Integer, ForeignKey('books.id') ,nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id') ,nullable=False, index=True)
    replay = Column(Integer, nullable=False, index=True, default="0")
    time = Column(String, nullable=False, index=True, default="none")

    book = db.relationship("Book", backref=backref("interactions" , lazy="dynamic"))
    user = db.relationship("User", backref=backref("interactions" , lazy="dynamic"))

    # types = [    activism   ,     comment     ,      replay     ]
    # types = [     review    ,    rejected     ,    confirmed    ]