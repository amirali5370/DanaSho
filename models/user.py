from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db
from flask_login import UserMixin
from sqlalchemy.types import ARRAY

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    username = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False, index=True)
    code = Column(Integer, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False, index=True)
    email = Column(String, nullable=False, index=True)
    grade = Column(String, nullable=False, index=True)
    birth = Column(String, nullable=False, index=True)  #1340 - 1397
    gender = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False, index=True)

    invite_code = Column(String, nullable=False, index=True)
    invite_auth = Column(String, nullable=False, index=True)
    msg_code = Column(Integer, index=True)

    
    province = Column(String, index=True)
    city = Column(String, index=True)
    school_name = Column(String, index=True)
    school_type = Column(String, index=True)
    home_addres = Column(String, index=True)
    recognition = Column(String, index=True)


    final = Column(Integer, default=0, index=True)
    authentication = Column(Integer, default=0, index=True)
    downloads = Column(Integer, default=2, index=True)

    
    coin = Column(Integer, default=0, index=True)
    point = Column(Integer, default=0, index=True)
    badge = Column(Integer, default=0, index=True)
    like = Column(Integer, default=0, index=True)
    invite = Column(Integer, default=0, index=True)


