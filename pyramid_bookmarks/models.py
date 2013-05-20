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

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(Unicode(255), unique=True, nullable=False)
  email = Column(Unicode(255), unique=True, nullable=False)
  password = Column(Unicode(255), nullable=False)
  last_logged = Column(DateTime, default=datetime.datetime.utcnow)

class Bookmark(Base):
  __tablename__ = 'bookmarks'
  id = Column(Integer, primary_key=True)
  owner_id = Column(Integer, ForeignKey('users.id'))
  title = Column(Unicode(255), nullable=False)
  url = Column(Unicode(512), nullable=False)
  created = Column(DateTime, default=datetime.datetime.utcnow)
  updated = Column(DateTime, default=datetime.datetime.utcnow)
