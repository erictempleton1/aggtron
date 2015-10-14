import requests
import unittest, datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from user_timeline import GetTimelineInfo

import sys
sys.path.insert(0, '../..')
import config

# global app scope
Session = sessionmaker()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron_test.db', echo=True)
Base = declarative_base()


class TestUserTimeline(unittest.TestCase):
    
    def setUp(self):

        # connect to db
        self.connection = engine.connect()

        # begin non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual session to connection
        self.session = Session(bind=self.connection)

        self.insta = GetTimelineInfo()
        self.timeline_url = 'https://api.instagram.com/v1/users/self/media/recent/'
        self.access_token = config.INSTAGRAM_TEST_TOKEN


        # create db and tables
        # ignored by default if db and table already exists
        Base.metadata.create_all(engine)

    def test_request(self):
        """
        test baseline request to the instagram API
        """
        base_req = self.insta.base_request(
                                           self.access_token,
                                           self.timeline_url
                                        )

        # test that the request can be made
        self.assertTrue(base_req)

        # test that the response contains actual user data
        self.assertTrue(u'user' in base_req['data'][0])
        

    def tearDown(self):
        self.session.close()

        # rollback everything committed above
        self.trans.rollback()

        # return connection to the engine
        self.connection.close()


if __name__ == '__main__':
    unittest.main()        