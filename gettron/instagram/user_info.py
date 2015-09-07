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


def query_auth_ids():
    auth_ids = [x.auth_id for x in session.query(UserInfo)]
    return auth_ids

print query_auth_ids()    