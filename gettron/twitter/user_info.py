import datetime
import requests
from requests_oauthlib import OAuth1
from models.user_info_model import AggTwitterUserInfo

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


# reflect existing tables
class UserInfo(Base):
    __table__ = Table('twitteruserinfoquery', metadata, autoload=True)

class AuthInfo(Base):
    __table__ = Table('authinfo', metadata, autoload=True)

class ProjectInfo(Base):
    __table__ = Table('project', metadata, autoload=True)


# create the session to use declared tables
session = Session()


class GetUserInfo(object):

    def __init__(self):
        self.queries = session.query(UserInfo)
        self.info_url = u'https://api.twitter.com/1.1/account/verify_credentials.json'

    def query_ids(self):
        """
        get all query ids from query table.
        mostly for testing purposes
        """

    def auth_ids(self):
        """
        get all auth ids from query table.
        mostly for testing purposes.
        """
        return [query.auth_ids for query in self.queries]

    def base_request(self, access_key, access_secret):
        """ set up request to twitter api """
        oauth_params = OAuth1(
                              config.TWITTER_CONSUMER_KEY,
                              config.TWITTER_CONSUMER_SECRET,
                              access_key,
                              access_secret
                            )

        try:
            r = requests.get(self.info_url, auth=oauth_params)
            json_result = r.json()   
        except AttributeError, e:
            # if the id does not exsit for some reason
            json_result = False
            print e
        yield json_result
    
    def get_token(self, auth_id):
        """ query for the access token from auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token.oauth_token
