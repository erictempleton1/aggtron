import requests
import datetime
from user_timeline_model import AggInstagramUserTimeline

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

import sys
sys.path.insert(0, '../..')
import config


# create engine and get metadata
Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=False)
metadata = MetaData(bind=engine)

# set session config
Session = sessionmaker()
Session.configure(bind=engine)


# reflect existing tables
class UserTimeline(Base):
    __table__ = Table('instagramuserfeedquery', metadata, autoload=True)


class AuthInfo(Base):
    __table__ = Table('authinfo', metadata, autoload=True)


class ProjectInfo(Base):
    __table__ = Table('project', metadata, autoload=True)

# create the session and use declared tables
session = Session()

class GetTimelineInfo(object):
    
    def __init__(self):
        self.queries = session.query(UserTimeline)
        self.timeline_url = 'https://api.instagram.com/v1/users/self/media/recent/'

    def base_request(self, access_token, url):
        """ set up request to instagram api """
        params = {'access_token': access_token}

        try:
            r = requests.get(url, params=params)
            yield r.json()
        except AttributeError, e:
            # if the id does not exist for some reason
            print 'Unable to complete request'
            print e    # switch to logging later

    def get_token(self, auth_id):
        """ query for access token from the auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token.oauth_token    

    def save_request(self):
        """
        make request to instagram api for user timeline.
        uses next url for page through results
        """
        # loop over all queries in user timeline table
        for query in self.queries:
            if query.enabled:

                print query.id

                # first get the access token
                access_token = self.get_token(query.auth_id)

                # set query url
                query_url = self.timeline_url

                # make the initial request
                insta_resp = self.base_request(access_token, query_url)

                count = 0

                # get the first page of results
                for res in insta_resp:
                    count += 1
                    print count
                    print res