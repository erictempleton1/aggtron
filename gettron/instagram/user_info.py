import requests
import datetime
from models.user_info_model import AggInstagramUserInfo

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
        """ 
        get all query ids from query table.
        mostly for testing purposes.
        """
        return [query.id for query in self.queries]

    def auth_ids(self):
        """
        get all auth ids from query table. 
        mostly for testing purposes.
        """
        return [query.auth_id for query in self.queries]

    def base_request(self, access_token):
        """ set up request to instagram api """
        params = {'access_token': access_token}

        try:
            r = requests.get(self.info_url, params=params)
            json_result = r.json()['data']
        except AttributeError, e:
            # if the id does not exist for some reason
            json_result = False
            print e    # switch to logging later
        yield json_result

    def get_token(self, auth_id):
        """ query for the access token from the auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token.oauth_token 

    def save_request(self):
        """
        make request to instagram api for user information.
        generator returns data in json format
        """
        # loop over all queries in user info table
        for query in self.queries:
            if query.enabled:

                # first get the access token
                access_token = self.get_token(query.auth_id)

                # get json response
                insta_info = self.base_request(access_token).next()

                insta_user_info = AggInstagramUserInfo(
                                                       query_id=query.id,
                                                       user_id=insta_info['id'],
                                                       username=insta_info['username'],
                                                       full_name=insta_info['full_name'],
                                                       profile_picture=insta_info['profile_picture'],
                                                       user_bio=insta_info['bio'],
                                                       user_website=insta_info['website'],
                                                       user_media=insta_info['counts']['media'],
                                                       user_follows=insta_info['counts']['follows'],
                                                       user_followers=insta_info['counts']['follows']
                                                    )
                session.add(insta_user_info)

                # update last run
                query.last_run = datetime.datetime.utcnow()

                try:
                    session.commit()
                except:
                    print 'Unable to save query: {0}'.format(query.name)    # switch logging later   

    def query_info_table(self):
        """ extra query for testing """
        usernames = [x.user_follows for x in session.query(AggInstagramUserInfo)]
        return usernames
            