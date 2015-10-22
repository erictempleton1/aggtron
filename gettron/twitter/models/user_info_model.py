import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=True)


class AggTwitterUserInfo(Base):

    __tablename__ = 'aggtwitteruserinfo'

    id = Column(Integer, primary_key=True)

    # query id from aggtron
    query_id = Column(Integer)

    # data from twitter API query response
    username = Column(String)
    user_id = Column(Integer)
    favorites_count = Column(Integer)
    listed_count = Column(Integer)
    followers_count = Column(Integer)
    statuses_count = Column(Integer)
    friends_count = Column(Integer)
    date = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return '<Username: {0}>'.format(self.username)


session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)        
