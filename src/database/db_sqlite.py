from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..contacts.models import Base

DBSession = None

def connect():
    global DBSession

    engine = create_engine('sqlite:///contacts.sqlite')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)


def get_database():
    if DBSession is None:
        connect()
    
    db = DBSession()

    try:
        yield db
    finally:
        db.close()