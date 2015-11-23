import datetime
import requests
from requests_oauthlib import OAuth1

import sys
sys.path.insert(0, '../../')
import config


class GetUserTimeline(object):

    def __init__(self):
        self.timeline_url = 'https://api.twitter.com/1.1/statuses/user_timeline.json'