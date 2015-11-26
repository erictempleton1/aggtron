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
from user_timeline import GetUserTimeline


# global app scope
Session = sessionmaker()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron_test.db', echo=True)
Base = declarative_base()


class TestTimelineQuery(unittest.TestCase):

    def setUp(self):

        # connect to db
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

        # create db and tables
        # ignored by default if db and table already exist
        Base.metadata.create_all(engine)

        self.user_timeline = GetUserTimeline(
            access_key=config.TWITTER_TEST_KEY,
            access_secret=config.TWITTER_TEST_KEY_SECRET
        )

        self.base_req =  self.user_timeline.base_request()

    def test_base_request(self):

        json_resp = self.base_req.next()

        print len(json_resp)   

        self.assertTrue(json_resp)

    def test_get_timeline(self):

        user_timeline = self.user_timeline.get_timeline()

        for tweet in user_timeline:
            print tweet


if __name__ == '__main__':
    unittest.main()             