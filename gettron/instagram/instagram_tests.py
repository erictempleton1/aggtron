import unittest
import requests

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData

from user_info import GetUserInfo
from user_info_model import AggInstagramUserInfo



# global app scope
Session = sessionmaker()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=True)
    

class TestInstagramQuery(unittest.TestCase):

    def setUp(self):

        # connect to db
        self.connection = engine.connect()

        # begin a non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)

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
        #print info_query
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

    def tearDown(self):
        self.session.close()

        # rollback everything from above
        self.trans.rollback()

        # return connection to the engine
        self.connection.close()        


if __name__ == '__main__':
    unittest.main()