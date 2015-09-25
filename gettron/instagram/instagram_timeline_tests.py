import requests
import unittest, datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

import sys
sys.path.insert(0, '../..')
import config

# global app scope
Session = sessionmaker()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron_test.db', echo=True)
Base = declarative_base()


def basic_query():
    params = {
                'access_token': config.INSTAGRAM_TEST_TOKEN,
                'count': 1
            }

    timeline_url = 'https://api.instagram.com/v1/users/self/media/recent/'
    r = requests.get(timeline_url, params)
    return r.json()

class TestUserTimeline(unittest.TestCase):
    
    def setUp(self):

        # connect to db
        self.connection = engine.connect()

        # begin non-ORM transaction
        self.trans = self.connection.begin()

        # bind an individual session to connection
        self.session = Session(bind=self.connection)

        # create db and tables
        # ignored by default if db and table already exists
        Base.metadata.create_all(engine)

    def tearDown(self):
        self.session.close()

        # rollback everything committed above
        self.trans.rollback()

        # return connection to the engine
        self.connection.close()


if __name__ == '__main__':
    unittest.main()        