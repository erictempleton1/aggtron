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
            return r.json()
        except AttributeError, e:
            # if the id does not exist for some reason
            print 'Unable to complete request'
            print e    # switch to logging later

    def get_token(self, auth_id):
        """ query for access token from the auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token.oauth_token    

    def make_request(self, access_token):
        """
        make request to instagram api for user timeline.
        uses next url for page through results
        """

        insta_resp = self.base_request(
                                       access_token,
                                       self.timeline_url
                                    )

        # url for next page provided in API results
        next_url = insta_resp['pagination']['next_url']

        # get the first page of results
        for res in insta_resp['data']:
            yield res

        while next_url is not None:

            # start a new request using the next_url defined above
            new_request = self.base_request(access_token, next_url)

            for res in new_request['data']:
                yield res

            # break out of the loop when there is no next_url        
            try:
                next_url = new_request['pagination']['next_url']
            except KeyError:
                break                

    def save_results(self):
        """
        loop over all queries and save
        """
        count = 0
        for query in self.queries:
            if query.enabled:

                # first get the access token
                access_token = self.get_token(query.auth_id)
                
                insta_json = self.make_request(access_token)

                for resp in insta_json:
                    count += 1
                    print count
                    
                    try:
                        img_text = resp['caption']['text']
                    except TypeError:
                        img_text = 'NA'

                    try:
                        longitude = resp['location']['latitude']
                        latitude = resp['location']['longitude']
                        location_name = resp['location']['name']
                    except TypeError:
                        longitude = 'NA'
                        latitude = 'NA'
                        location_name = 'NA'        

                    comment_count = resp['comments']['count']
                    created_time = resp['created_time']
                    img_filter = resp['filter']
                    img_thumb_url = resp['images']['thumbnail']['url']
                    img_stand_url = resp['images']['standard_resolution']['url']
                    img_tag = ' '.join(resp['tags'])   # split list into one word strings
