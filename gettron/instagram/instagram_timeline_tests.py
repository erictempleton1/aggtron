import requests
import unittest, datetime

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

import sys
sys.path.insert(0, '../..')
import config


def basic_query():
    params = {
                'access_token': config.INSTAGRAM_TEST_TOKEN,
                'count': 1
            }
            
    timeline_url = 'https://api.instagram.com/v1/users/self/media/recent/'
    r = requests.get(timeline_url, params)
    return r.json()

class TestUserTimeline(unittest.TestCase):
    pass