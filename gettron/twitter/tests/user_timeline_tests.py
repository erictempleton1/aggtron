import requests
import unittest
import datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData

import sys
sys.path.insert(0, '../../..')
import config
sys.path.insert(0, '../')
from user_timeline import GetUserTimeline, UserTimelineHandlers, UserTimeline, QueryHandlers


# global app scope
Session = sessionmaker()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron_test.db', echo=True)
Base = declarative_base()

# todo seperate test classes to match user_timeline.py classes

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

        # set up base request
        self.user_timeline = GetUserTimeline(
            access_key=config.TWITTER_TEST_KEY,
            access_secret=config.TWITTER_TEST_KEY_SECRET
        )
        self.base_req =  self.user_timeline.base_request()

        # set up query handlers
        self.query_handlers = QueryHandlers()


    def test_base_request(self):
        """
        Test top level query to the api
        """
        json_resp = self.base_req.next()

        print len(json_resp)   

        self.assertTrue(json_resp)

    def test_get_timeline(self):
        """
        Test response from the api for as much of the timeline as possible
        """
        query_timeline = self.user_timeline.get_timeline()

        # user generator to get first page of results
        user_timeline = query_timeline.next()

        print user_timeline
        # tweet text in the dict indicates good response
        self.assertTrue('text' in user_timeline)

    def test_get_recent(self):
        """
        Test that tweets after a given ID are returned
        """
        pass

    def test_get_queries(self):
        """
        Test that queries are returned
        """
        queries = self.query_handlers.get_queries()
        for q in queries:
            print q.name

        self.assertTrue(queries)

    def test_get_tokens(self):
        """
        Test that given token is returned
        """
        # grab a recent id
        auth_id = self.query_handlers.get_queries().first().id

        # query for token based on that id
        token = self.query_handlers.get_tokens(auth_id)

        oauth_token = token.oauth_token
        oauth_token_secret = token.oauth_token_secret

        print oauth_token, oauth_token_secret
        self.assertTrue(oauth_token)
        self.assertTrue(oauth_token_secret)

    def test_save_tweets(self):
        """
        Test save method
        """
        query_timeline = self.user_timeline.get_timeline()

        timeline_handler = UserTimelineHandlers(query_timeline)

        timeline_handler.save_tweets()

    def tearDown(self):
        self.session.close()

        # rollback everything from above
        self.trans.rollback()

        # return connection to the engine
        self.connection.close()


if __name__ == '__main__':
    unittest.main()             