import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=True)


class AggInstagramUserInfo(Base):

    __tablename__ = 'agginstagramuserinfo'

    id = Column(Integer, primary_key=True)

    # project and query id from aggtron
    query_id = Column(Integer)

    # data from instagram API query response
    user_id = Column(Integer)
    username = Column(String(250))
    full_name = Column(String(250))
    profile_picture = Column(String)
    user_bio = Column(String)
    user_website = Column(String)
    user_media = Column(Integer)
    user_follows = Column(Integer)
    user_followers = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Username: {0}>'.format(self.username)


session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)        