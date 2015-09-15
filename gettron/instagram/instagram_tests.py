import unittest
import requests

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData

from user_info import query_auth_ids
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
                                        project_id=1,
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

    def test_query_id(self):
        print query_auth_ids()
        self.assertTrue(len(query_auth_ids()) > 0)    

    def tearDown(self):
        self.session.close()

        # rollback everything from above
        self.trans.rollback()

        # return connection to the engine
        self.connection.close()        


if __name__ == '__main__':
    unittest.main()