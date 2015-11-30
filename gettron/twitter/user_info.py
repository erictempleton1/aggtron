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
        self.info_url = 'https://api.twitter.com/1.1/account/verify_credentials.json?skip_status=true'

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

    def get_tokens(self, auth_id):
        """ query for the access token from auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token

    def save_request(self):
        """
        make request to twitter api for verify_credentials
        """
        # iterate all queries in user info table
        for query in self.queries:
            if query.enabled:

              # get the access tokens
              access_token = self.get_tokens(query.auth_id)

              # get json response from request generator
              twitter_info = self.base_request(
                                            access_token.oauth_token,
                                            access_token.oauth_token_secret
                                          ).next()

              twitter_user_info = AggTwitterUserInfo(
                                                     query_id=query.id,
                                                     username=twitter_info['name'],
                                                     user_id=twitter_info['id'],
                                                     favorites_count=twitter_info['favourites'],
                                                     listed_count=twitter_info['listed_count'],
                                                     followers_count=twitter_info['followers_count'],
                                                     statuses_count=twitter_info['statuses_count'],
                                                     friends_count=twitter_info['friends_count']
                                                  )
              session.add(twitter_user_info)

            # update last run
            query.last_run = datetime.datetime.utcnow()

        session.commit()
