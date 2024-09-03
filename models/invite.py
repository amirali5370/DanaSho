from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Invite(db.Model):
    __tablename__ = "invites"
    id = Column(Integer, primary_key=True)
    inviter_id = Column(Integer, ForeignKey('users.id') ,nullable=False, index=True)
    invitee_id = Column(Integer, nullable=False, index=True)
    invitee = Column(String, nullable=False, index=True)


    my_inverter = db.relationship("User", backref=backref("invites" , lazy="dynamic"))