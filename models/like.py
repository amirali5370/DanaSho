from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Like(db.Model):
    __tablename__ = "likes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id') ,nullable=False, index=True)
    activism_id = Column(Integer, ForeignKey('interactions.id') ,nullable=False, index=True)

    user = db.relationship("User", backref=backref("likes" , lazy="dynamic"))
    activism = db.relationship("Interaction", backref=backref("likes" , lazy="dynamic"))
