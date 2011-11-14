# -*- coding: utf-8 -*-
from config import DEFAULT_USER_PORTRAIT_PATH
from database import Base, db_session
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship, backref
from datetime import datetime

class BaseModel():
    @classmethod
    def get(cls, id):
        return cls.query.get(id)
    def save(self):
        if self.id is None:
            db_session.add(self)
        db_session.commit()

class User(Base, BaseModel):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    portrait = Column(String(100), default=DEFAULT_USER_PORTRAIT_PATH)
    renren_id = Column(Integer, unique=True, nullable=True)
    weibo_id = Column(Integer, unique=True, nullable=True)
    douban_id = Column(Integer, unique=True, nullable=True)
    qq_id = Column(Integer, unique=True, nullable=True)
    taobao_id = Column(Integer, unique=True, nullable=True)
    def __init__(self, name, portrait):
        self.name = name
        self.portrait = portrait
    def __repr__(self):
        return self.name

#产品
class Product(Base, BaseModel):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))   
    picture = Column(String(100), nullable=False)
    description = Column(String(140))
    link = Column(String(100))
    user_id = Column(Integer, ForeignKey('user.id'))
    share_by = relationship('User', backref='product_shared')
    
#产品的likes    
class Likes(Base):
    __tablename__ = 'product_likes'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship('User', backref='likes') 
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product = relationship('Product', backref='likes')
    
#产品的购买意向    
class Purchase(Base):
    __tablename__ = 'product_purchase'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship('User', backref='purchase') 
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product = relationship('Product', backref='purchase')

#拥有产品    
class Own(Base):
    __tablename__ = 'product_own'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    user = relationship('User', backref='own') 
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)
    product = relationship('Product', backref='own')    