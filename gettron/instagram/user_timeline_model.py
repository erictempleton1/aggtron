import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=True)


class AggInstagramUserTimeline(Base):

    __tablename__ = 'agginstagramusertimeline'

    id = Column(Integer, primary_key=True)

    # project and query id from aggtron
    query_id = Column(Integer)

    # data from instagram API query response
    img_text = Column(String)
    comment_count = Column(Integer)
    created_time = Column(Integer)
    img_filter = Column(String)
    img_thumb_url = Column(String)
    img_std_url = Column(String)
    img_likes = Column(Integer)
    longitude = Column(Integer)
    lattitude = Column(Integer)
    location_name = Column(String)
    img_tag = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)


    def __repr__(self):
        return '<Caption: {0}>'.format(self.caption)


# bind session and create table 
# if it doesn't exist
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)