from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Interaction(db.Model):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, index=True)
    status = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id') ,nullable=False, index=True)
    replay = Column(String, nullable=False, index=True)
    time = Column(Integer, nullable=False, index=True)

    user = db.relationship("User", backref=backref("interactions" , lazy="dynamic"))