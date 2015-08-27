from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create engine and get metadata
Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=True)
metadata = MetaData(bind=engine)

# set session config
Session = sessionmaker()
Session.configure(bind=engine)


# reflect the table for projects
class Project(Base):
    __table__ = Table('project', metadata, autoload=True)


class TwitterUserTimelineQuery(Base):
    __table__ = Table('twitterusertimelinequery', metadata, autoload=True)


# create the session to use declared tables
session = Session()

# basic query to get all of the data from the declared table
project_query = session.query(TwitterUserTimelineQuery).all()

# list project names from above query
for x in project_query:
    print x.name