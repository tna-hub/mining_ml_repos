from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/ml_repos')
Base = declarative_base()
Base.metadata.reflect(engine)
session = scoped_session(sessionmaker(bind=engine))


# The Repo model represents the repos table
class Repo(Base):
    __table__ = Base.metadata.tables['element']


# querying the model and getting results
query = session.query(Repo)
for repo in query.all():
    print('id:{} , name:{}'.format(repo.id, repo.link))
