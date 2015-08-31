from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# create engine and get metadata
Base = declarative_base()
engine = create_engine('sqlite:////home/erictempleton/Documents/Projects/myenv/aggtron/aggtron.db', echo=True)

# set session config
Session = sessionmaker()
Session.configure(bind=engine)

# reflect user info table
class UserInfo(Base):
    __table__ = Table('instagramuserinfoquery', metadata, autoload=True)



# create the session to use declared tables
session = Session()

print metadata.tables.keys()