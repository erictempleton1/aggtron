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

        self.user_info = GetUserInfo()
        self.base_req = self.user_info.base_request(
                                                    config.TWITTER_TEST_KEY,
                                                    config.TWITTER_TEST_KEY_SECRET
                                                )
        self.json_resp = self.base_req.next()

    def test_base_request(self):
        """ test basic request to the twitter API """
        print self.json_resp
        self.assertTrue(self.json_resp)

    def test_get_token(self):
        """
        test to be sure something is returned from auth token query
        """
        self.assertTrue(self.user_info.get_tokens(1))

    def test_get_results(self):
        resp_data = self.json_resp
        print resp_data['followers_count']
        print resp_data['id']
        print resp_data['listed_count']
        print resp_data['favourites_count']
        print resp_data['friends_count']
        print resp_data['statuses_count']
        self.assertTrue(resp_data)
        
    def tearDown(self):
        self.session.close()

        # rollback everything from above
        self.trans.rollback()

        # return the connection to the engine
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
