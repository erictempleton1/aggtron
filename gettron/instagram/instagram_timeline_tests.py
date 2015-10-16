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
metadata = MetaData(bind=engine)


class AggInstagramUserTimeline(Base):
    """ create table for testing """

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
        return '<Img Text: {0}>'.format(self.img_text)


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
        self.assertTrue('user' in base_req['data'][0])

    def test_make_request(self):
        """
        test that the generator is initiated and
        that the response contains user data
        """
        make_req = self.insta.make_request(self.access_token)

        # tags key should always be present in the API response
        self.assertTrue('tags' in make_req.next())

    def test_save_results(self):
        pass
                   
    def tearDown(self):
        self.session.close()

        # rollback everything committed above
        self.trans.rollback()

        # return connection to the engine
        self.connection.close()


if __name__ == '__main__':
    unittest.main()        