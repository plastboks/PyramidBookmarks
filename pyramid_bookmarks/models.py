import datetime
import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    ForeignKey,
    )

from cryptacular.bcrypt import BCRYPTPasswordManager
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

from webhelpers.text import urlify
from webhelpers.paginate import PageURL_WebOb, Page
from webhelpers.date import time_ago_in_words


DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(Unicode(255), unique=True, nullable=False)
  email = Column(Unicode(255), unique=True, nullable=False)
  password = Column(Unicode(255), nullable=False)
  last_logged = Column(DateTime, default=datetime.datetime.utcnow)

  @classmethod
  def by_username(cls, username):
    return DBSession.query(User).filter(User.username == username).first()

  def verify_password(self, password):
    manager = BCRYPTPasswordManager()
    return manager.check(self.password, password)

class Bookmark(Base):
  __tablename__ = 'bookmarks'
  id = Column(Integer, primary_key=True)
  owner_id = Column(Integer, ForeignKey('users.id'))
  title = Column(Unicode(255), nullable=False)
  url = Column(Unicode(512), nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)
  
  @classmethod
  def all(cls):
    return DBSession.query(Bookmark).order_by(sa.desc(Bookmark.created))

  @classmethod
  def by_id(cls, id):
    return DBSession.query(Bookmark).filter(Bookmark.id == id).first()

  @property
  def slug(self):
    return urlify(self.title)

  @property
  def created_in_words(self):
    return time_ago_in_words(self.created)

  @classmethod
  def get_paginator(cls, request, page=1):
    page_url = PageURL_WebOb(request)
    return Page(Bookmark.all(), page, url=page_url, items_per_page=5)
