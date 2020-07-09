from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import configparser
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

Base = declarative_base()


def init_db(config_file='/home/ubuntu/PycharmProjects/mining_ml_repos/data/config.ini', echo=False):
    config = configparser.ConfigParser()
    config.read(config_file)

    host = config['postgresql']['host']
    user = config['postgresql']['user']
    passwd = config['postgresql']['passwd']
    db = config['postgresql']['db']
    engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(user,
                                                                      passwd,
                                                                      host,
                                                                      db),
                           echo=echo)
    return engine


Session = sessionmaker(bind=init_db())


@contextmanager
def session_scope():
    """Provide a transactional scope for the operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    #finally:
        #session.close()