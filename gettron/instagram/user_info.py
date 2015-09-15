from sqlalchemy.orm import sessionmaker
from user_info_model import AggInstagramUserInfo
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base

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

def get_project_info():
    # get all instagram projects
    # might not be needed
    proj_ids = [x.id for x in session.query(ProjectInfo).filter(ProjectInfo.api_type == 'Instagram')]
    return proj_ids

def query_auth_ids():
    auth_ids = [x.id for x in session.query(AuthInfo)]
    return auth_ids

def get_queries():
    insta_queries = [x.id for x in session.query(UserInfo)]
    return insta_queries

print query_auth_ids()
print get_project_info()
print get_queries()

