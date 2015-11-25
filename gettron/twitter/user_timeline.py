import datetime
import requests
from requests_oauthlib import OAuth1

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

import sys
sys.path.insert(0, '../../')
import config

# create engine and get metadata
Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=False)
metadata = MetaData(bind=engine)

# set session config
Session = sessionmaker()
Session.configure(bind=engine)


# reflect exsiting tables
class UserTimeline(Base):
    __table__ = Table('twitterusertimelinequery', metadata, autoload=True)

class AuthInfo(Base):
    __table__ = Table('authinfo', metadata, autoload=True)

class ProjectInfo(Base):
   __table__ = Table('project', metadata, autoload=True)

# create the session to use declared tables
session = Session()


class GetUserTimeline(object):

    def __init__(self):
        self.queries = session.query(UserTimeline)
        self.timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

    def base_request(self, access_key, access_secret, max_id=None):
        """ set up request to twitter api """
        oauth_params = OAuth1(
                              config.TWITTER_CONSUMER_KEY,
                              config.TWITTER_CONSUMER_SECRET,
                              access_key,
                              access_secret
                            )

        params = {
            'count': '200',
            'max_id': max_id
        }
        try:
            r = requests.get(self.timeline_url, auth=oauth_params, params=params)
            json_result = r.json()
        except AttributeError, e:
            # if the id does not exist for some reason
            json_result = False
            print e
        yield json_result 
        
    def get_tokens(self, auth_id):
        """ query for access token from auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token                                  