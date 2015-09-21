import requests
import unittest, datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from user_info import GetUserInfo

import sys
sys.path.insert(0, '../..')
import config


# global app scope
Session = sessionmaker()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron_test.db', echo=True)
Base = declarative_base()


class AggInstagramUserInfo(Base):
    """ re-create user info table for testing """

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


class TestInstagramQuery(unittest.TestCase):

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

    def test_save(self):
        new_info = AggInstagramUserInfo(
                                        query_id=2,
                                        user_id=1,
                                        full_name='eric',
                                        profile_picture='example.com',
                                        user_bio='example.com',
                                        user_website='example.com',
                                        user_media=345,
                                        user_follows=789,
                                        user_followers=3478
                                    )
        self.session.add(new_info)
        self.session.commit()
        info_query = self.session.query(AggInstagramUserInfo)
        self.assertTrue(info_query)

    def test_query_auth_len(self):
        """
        need to be sure that there are the same number of query ids
        as there are auth ids.
        """
        info = GetUserInfo()
        self.assertEqual(len(info.query_ids()), len(info.auth_ids()))

    def test_get_token(self):
        auth_token = GetUserInfo()
        self.assertTrue(auth_token.get_token(1))

    def test_base_request(self):
        info = GetUserInfo()
        auth_token = config.INSTAGRAM_TEST_TOKEN
        base_req = info.base_request(auth_token)
        self.assertTrue('username' in base_req.next())                 

    def tearDown(self):
        self.session.close()

        # rollback everything from above
        self.trans.rollback()

        # return connection to the engine
        self.connection.close()      


if __name__ == '__main__':
    unittest.main()

