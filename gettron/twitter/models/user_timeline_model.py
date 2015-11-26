import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime


Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=True)

class AggTwitterUserTimeline(Base):

    __tablename__ = 'aggtwitterusertimeline'

    id = Column(Integer, primary_key=True)

    # query id from aggtron
    query_id = Column(Integer)

    # data from twitter API query response
    tweet_id = Column(Integer)
    created_at = Column(String)
    coordinate_lat = Column(Integer)
    coordinate_long = Column(Integer)
    favorite_count = Column(Integer)
    in_reply_to_screen_name = Column(String)
    in_reply_to_status_id = Column(Integer)
    in_reply_to_user_id = Column(Integer)
    place_name = Column(String)
    quoted_status_id = Column(Integer)
    quoted_status = Column(String)
    retweet_count = Column(Integer)
    tweet_text = Column(String)

    def __repr__(self):
        return '<Tweet Id: {0}>'.format(self.tweet_id)


session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
