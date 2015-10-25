import requests
import unittest
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

import sys
sys.path.insert(0, '../../..')
import config
sys.path.insert(0, '../')
from user_info import GetUserInfo


# global app scope
Session = sessionmaker()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron_test.db', echo=True)
Base = declarative_base()


class AggTwitterUserInfo(Base):
    """ re-create user info table for testing """

    __tablename__ = 'aggtwitteruserinfo'

    id = Column(Integer, primary_key=True)

    # project query id from aggtron
    query_id = Column(Integer)
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


class TestTwitterQuery(unittest.TestCase):

    def setUp(self):

        # connect to db
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

        # create db and tables
        # ignored by default if db and table already exists
        Base.metadata.create_all(engine)

    def test_base_request(self):
        """ test basic request to the twitter API """
        info = GetUserInfo()
        auth_token = config.TWITTER_TEST_TOKEN
        base_req = info.base_request(auth_token)
        print base_req.next()

    def tearDown(self):
        self.session.close()

        # rollback everything from above
        self.trans.rollback()

        # return the connection to the engine
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
