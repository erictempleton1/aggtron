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

        self.user_timeline = GetUserTimeline()

        self.base_req =  self.user_timeline.base_request(
                                                    access_key=config.TWITTER_TEST_KEY,
                                                    access_secret=config.TWITTER_TEST_KEY_SECRET
                                                )

    def test_base_request(self):

        json_resp = self.base_req.next()

        print len(json_resp)   

        self.assertTrue(json_resp)

    def test_get_all(self):
        """
        get the last id in the returned list, subtract one from that id, 
        and use it in the max_id param to query as many tweets as possible.
        """
        count = 0

        # make initial request for the first 200 results
        make_req = self.base_req.next()

        for x in make_req:
            count += 1
            print count
            print x

        # get the last id from the list
        max_id = make_req[-1]['id']

        # api docs say to subtract one from the id and query again using that id as the next id
        next_max = max_id - 1

        while max_id:

            # make the query again using next_max
            base_req = self.user_timeline.base_request(
                config.TWITTER_TEST_KEY,
                config.TWITTER_TEST_KEY_SECRET,
                next_max
            )

            make_req = base_req.next()

            for x in make_req:
                count += 1
                print count
                print x

            try:
                # keep trying to get the max_id until some limit is hit, then break out of the loop
                # could be a quota limit, 3200 tweet limit, or we got all tweets
                max_id = make_req[-1]['id']
                next_max = max_id - 1
            except Exception, e:
                print e
                max_id = False


if __name__ == '__main__':
    unittest.main()             