import datetime
import requests
from requests_oauthlib import OAuth1
from models.user_timeline_model import AggTwitterUserTimeline

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

    def __init__(self, access_key, access_secret):
        self.access_key = access_key
        self.access_secret = access_secret
        self.timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

    def base_request(self, max_id=None, since_id=None):
        """ set up request to twitter api """
        oauth_params = OAuth1(
                              config.TWITTER_CONSUMER_KEY,
                              config.TWITTER_CONSUMER_SECRET,
                              self.access_key,
                              self.access_secret
                            )
        params = {
            'count': '200',
            'max_id': max_id,
            'since_id': since_id,
            'trim_user': 1
        }

        try:
            r = requests.get(self.timeline_url, auth=oauth_params, params=params)
            json_result = r.json()
        except AttributeError, e:
            # if the id does not exist for some reason
            json_result = False
            print e
        yield json_result

    def get_timeline(self):
        """
        Make requests to get as much of the user's timeline as possible
        """
        # make initial request for first 200 results
        make_req = self.base_request().next()

        for res in make_req:
            yield res

        # get the last if from the list
        max_id = make_req[-1]['id']

        # subtract one from max_id and use this to query next 200
        next_max = max_id - 1

        while max_id:

            # make the query again using next_max
            base_req = self.base_request(
                max_id=next_max
            )

            make_req = base_req.next()

            for res in make_req:
                yield res

            try:
                # keep trying to get the max_id until some limit is hit, then break out of the loop
                # could be a quota limit, 3200 tweet limit, or we got all tweets
                max_id = make_req[-1]['id']
                next_max = max_id - 1
            except Exception:
                max_id = False

    def get_recent(self, since_id):
        """
        Query for any new tweets since last saved tweet
        """
        since_req = self.base_request(since_id)

        for res in since_req:
            yield res


class QueryHandlers(object):

    def get_queries(self):
        """
        Return active queries from db
        """
        queries = session.query(UserTimeline)
        return queries

    def get_tokens(self, auth_id):
        """ query for access token from auth info table """
        access_token = session.query(AuthInfo).filter_by(id=auth_id).first()
        return access_token

    def query_recent(self):
        """
        Query db for last saved tweet
        """
        # AggTwitterUserTimeline.query.filter_by(query_id).first() ...?
        pass


class UserTimelineHandlers(object):

    def __init__(self, tweet_list, max_id=None, since_id=None):
        self.tweet_list = tweet_list
        self.queries = session.query(UserTimeline)
        self.max_id=max_id
        self.since_id=since_id

    def save_tweets(self):
        """
        Iterate over twitter response and save
        """
        count = 0
        for query in self.queries:
            for tweet in self.tweet_list:

                tweet_id = tweet['id']
                tweet_text = tweet['text'].encode('utf-8')
                created_at = tweet['created_at']
                fav_count = tweet['favorite_count']
                retweet_count = tweet['retweet_count']

                try:
                    coordinate_lat = tweet['coordinates']['coordinates'][0]
                    coordinate_long = tweet['coordinates']['coordinates'][1]
                except TypeError:
                    coordinate_lat = 0
                    coordinate_long = 0

                try:
                    place_name = tweet['place']['name']
                except TypeError:
                    place_name = 'NA'

                try:
                    quoted_status_id = tweet['quoted_status_id']
                    quoted_status = unicode(tweet['quoted_status']['text'])
                except KeyError:
                    quoted_status_id = 0
                    quoted_status = 'NA'

                try:
                    reply_to_name = tweet['in_reply_to_screen_name']
                    reply_to_status_id = tweet['in_reply_to_status_id']
                    reply_to_user_id = tweet['in_reply_to_user_id']
                except KeyError:
                    reply_to_name = 'NA'
                    reply_to_status_id = 0
                    reply_to_user_id = 0

                twitter_timeline = AggTwitterUserTimeline(
                    query_id=query.id,
                    tweet_id=tweet_id,
                    created_at=created_at,
                    coordinate_lat=coordinate_lat,
                    coordinate_long=coordinate_long,
                    favorite_count=fav_count,
                    in_reply_to_screen_name=reply_to_name,
                    in_reply_to_status_id=reply_to_status_id,
                    in_reply_to_user_id=reply_to_user_id,
                    place_name=place_name,
                    quoted_status_id=quoted_status_id,
                    quoted_status=str(quoted_status),
                    retweet_count=retweet_count,
                    tweet_text=str(tweet_text)
                )
                count += 1
                print count

                session.add(twitter_timeline)

            # update last run
            query.last_run = datetime.datetime.utcnow()

        session.commit()
