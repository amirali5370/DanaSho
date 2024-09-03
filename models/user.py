from sqlalchemy import *
from sqlalchemy.orm import backref
from extentions import db

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=False, index=True )
    code = Column(Integer, unique=True, nullable=False, index=True)
    grade = Column(String, nullable=False, index=True)
    birth = Column(String, nullable=False, index=True)  #1340 - 1397
    gender = Column(Integer, nullable=False, index=True)
    type = Column(Integer, nullable=False, index=True)

    
    province = Column(Integer, index=True)
    city = Column(Integer, index=True)
    school_name = Column(String, index=True)
    school_type = Column(String, index=True)
    home_addres = Column(String, index=True)


    final = Column(String, index=True)
    completion = Column(String, index=True)
    downloads = Column(String, index=True)

    
    coin = Column(Integer, nullable=False, index=True)
    point = Column(Integer, nullable=False, index=True)
    badge = Column(Integer, nullable=False, index=True)
    invite = Column(Integer, nullable=False, index=True)
    invite_list = Column(ARRAY(Integer) , nullable=False, index=True)


