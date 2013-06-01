from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import (
    Column,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    DateTime,
    ForeignKey,
    or_,
    and_,
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

##############
# User Class #
##############
class User(Base):

  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(Unicode(255), unique=True, nullable=False)
  email = Column(Unicode(255), unique=True, nullable=False)
  password = Column(Unicode(255), nullable=False)
  last_logged = Column(DateTime, default=datetime.utcnow)

  pm = BCRYPTPasswordManager()

  @classmethod
  def by_id(cls, id):
    return DBSession.query(User).filter(User.id == id).first()

  @classmethod
  def by_uname_email(cls, login):
    return DBSession.query(User).filter(or_(User.username == login,\
                                            User.email == login))\
                                .first()

  def verify_password(self, password):
    return self.pm.check(self.password, password)

  def hash_password(self, password):
    return self.pm.encode(password)

  def my(self):
    return DBSession.query(Bookmark).filter(Bookmark.owner_id == self.id)

  def bookmarks(self, request, page=1):
    page_url = PageURL_WebOb(request)
    return Page(self.my().all(), page, url=page_url, items_per_page=12)

  def bookmark(self, id):
    return self.my().filter(Bookmark.id == id).first()

  def bookmark_tags(self, request, string='', page=1):
    page_url = PageURL_WebOb(request)
    tag = "%"+string+"%"
    bookmarks = self.my().filter(Bookmark.tags.like(tag)).all()
    return Page(bookmarks, page, url=page_url, items_per_page=12)

  def bookmark_search(self, request, string='', page=1):
    page_url = PageURL_WebOb(request)
    string = "%"+string+"%"
    bookmarks = self.my().filter(or_(Bookmark.title.like(string),\
                                     Bookmark.url.like(string))).all()
    return Page(bookmarks, page, url=page_url, items_per_page=12)


##################
# Bookmark Class #
##################
class Bookmark(Base):
  __tablename__ = 'bookmarks'
  id = Column(Integer, primary_key=True)
  owner_id = Column(Integer, ForeignKey('users.id'))
  title = Column(Unicode(255), nullable=False)
  url = Column(Unicode(512), nullable=False)
  tags = Column(Unicode(512))
  created = Column(DateTime, default=datetime.utcnow)
  updated = Column(DateTime, default=datetime.utcnow)
  
  @classmethod
  def all(cls):
    return DBSession.query(Bookmark).order_by(sa.desc(Bookmark.created))

  @property
  def slug(self):
    return urlify(self.title)

  @property
  def created_in_words(self):
    return time_ago_in_words(self.created)

