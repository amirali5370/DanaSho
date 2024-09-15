from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False, index=True)
    sub_type = Column(String, index=True)
    content = Column(String, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id') ,nullable=False, index=True)
    time = Column(Integer, nullable=False, index=True)

#   types={ admin : [ -invited , coin_confirm* , comment_sta*],
#            user : [ request* , excerpt      ]}
    user = db.relationship("User", backref=backref("tickets" , lazy="dynamic"))