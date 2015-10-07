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

                # so we can keep track of where we are
                count = 0

                # url for next page provided in API results
                next_url = insta_resp['pagination']['next_url']

                # get the first page of results
                for res in insta_resp['data']:
                    count += 1
                    print count

                    # account for possible missing values
                    try:
                        img_text = res['caption']['text']
                    except TypeError:
                        img_text = 'NA'

                    try:
                        location_name = res['location']['name']
                    except TypeError:
                        location_name = 'NA'

                    try:
                        longitude = res['location']['longitude']
                        latitude = res['location']['latitude']
                        location_name = res['location']['name']
                    except TypeError:
                        longitude = 'NA'
                        latitude = 'NA'
                        location_name = 'NA'     

                    created_time = res['created_time']
                    img_filter = res['filter']
                    img_likes = res['likes']['count']
                    comment_count = res['comments']['count']

                    # tags are sent as a list in the response, and are always one word
                    # joining them by a space allows them to be saves and parsed later
                    img_tag = ' '.join(res['tags'])

                    # first part of url is the same, so no need to save it
                    img_thumb_url = res['images']['thumbnail']['url'][34:]
                    img_std_url = res['images']['standard_resolution']['url'][34:]

                    insta_user_timeline = AggInstagramUserTimeline(
                                                       img_text=img_text,
                                                       comment_count=comment_count,
                                                       created_time=created_time,
                                                       img_filter=img_filter,
                                                       img_thumb_url=img_thumb_url,
                                                       img_std_url=img_std_url,
                                                       longitude=longitude,
                                                       lattitude=latitude,
                                                       location_name=location_name
                                                    )
                    
                    # update last run
                    query.last_run = datetime.datetime.utcnow()

                    session.add(insta_user_timeline)
                    session.commit()

                while next_url is not None:

                    # start a new request using the next_url defined above
                    new_request = self.base_request(access_token, next_url)

                    for res in new_request['data']:
                        count += 1
                        print count
                        try:
                            img_text = res['caption']['text']
                        except TypeError:
                            img_text = 'NA'

                        try:
                            location_name = res['location']['name']
                        except TypeError:
                            location_name = 'NA'

                        try:
                            longitude = res['location']['longitude']
                            latitude = res['location']['latitude']
                            location_name = res['location']['name']
                        except TypeError:
                            longitude = 'NA'
                            latitude = 'NA'
                            location_name = 'NA'

                        created_time = res['created_time']
                        comment_count = res['comments']['count']
                        img_filter = res['filter']
                        img_thumb_url = res['images']['thumbnail']['url'][34:]
                        img_std_url = res['images']['standard_resolution']['url'][34:]
                        img_likes = res['likes']['count']
                        img_tag = ' '.join(res['tags']) 

                        insta_user_timeline = AggInstagramUserTimeline(
                                                       img_text=img_text,
                                                       comment_count=comment_count,
                                                       created_time=created_time,
                                                       img_filter=img_filter,
                                                       img_thumb_url=img_thumb_url,
                                                       img_std_url=img_std_url,
                                                       longitude=longitude,
                                                       lattitude=latitude,
                                                       location_name=location_name
                                                    )

                        session.add(insta_user_timeline)
                        session.commit()

                    # break out of the loop when there is no next_url        
                    try:
                        next_url = new_request['pagination']['next_url']
                    except KeyError:
                        break   
