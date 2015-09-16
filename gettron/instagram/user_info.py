import requests
from sqlalchemy.orm import sessionmaker
from user_info_model import AggInstagramUserInfo
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
class UserInfo(Base):
    __table__ = Table('instagramuserinfoquery', metadata, autoload=True)


class AuthInfo(Base):
    __table__ = Table('authinfo', metadata, autoload=True)


class ProjectInfo(Base):
    __table__ = Table('project', metadata, autoload=True)
 

# create the session to use declared tables
session = Session()


class GetUserInfo(object):


    def __init__(self):
        self.queries = session.query(UserInfo)
        self.info_url = 'https://api.instagram.com/v1/users/self/'

    def query_ids(self):
        """ get all query ids from query table """
        return [query.id for query in self.queries]

    def auth_ids(self):
        """ get all auth ids from query table """
        return [query.auth_id for query in self.queries]

    def insta_request(self, access_token):
        """ set up request to instagram api """
        params = {'access_token': access_token}

        try:
            r = requests.get(self.info_url, params=params)
            json_result = r.json()
        except AttributeError, e:
            # if the id does not exist for some reason
            json_result = False
            print e    # switch to logging later
        return json_result

    def get_token(self, auth_id):
        """ query for the access token from the auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token.oauth_token       

    def make_request(self):
        """
        make request to instagram api for user information.
        generator returns data in json format
        """
        # loop over all queries in user info table
        for query in self.queries:
            if query.enabled:

                # first get the access token
                access_token = self.get_token(query.auth_id)

                # return json api results
                yield self.insta_request(access_token)
            