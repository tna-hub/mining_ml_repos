import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Using automap extension
from sqlalchemy.ext.automap import automap_base
from git import Repo as rp

import get_ast

from utils import File

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/ml_repos')
Base = automap_base()
Base.prepare(engine, reflect=True)
session = scoped_session(sessionmaker(bind=engine))


class Repo(Base):
    __table__ = Base.metadata.tables['repos']

    @classmethod
    def by_id(cls, repo_id):
        return session.query(Repo).filter(Repo.id == repo_id).one()

    def download(self):
        try:
            if not os.path.isdir(self.folder_name):
                rp.clone_from(self.link, self.folder_name)
            return True
        except Exception as e:
            print(e)
            return False

    @classmethod
    def get_elements(cls):
        return session.query(Element).filter(Element.repo_id == Repo.id).all()

    def extract_elements(self):
        for r, d, f in os.walk(self.folder_name):
            for file in f:
                path = os.path.join(r, file)
                el = Element(
                    is_folder=False,
                    name=path,
                    repo_id=self.id
                )
                el.extension = el.get_extension()
                el.is_code_file = el.set_is_code_file()
                if el.is_code_file:
                    el.ast = el.set_ast()
                    print("thi is ast", el.ast)
                if not el.ignore():
                    # print(el.name, el.is_code_file)
                    session.add(el)
                    session.commit()
                    session.flush()

            for folder in d:
                path = os.path.join(r, folder)
                el = Element(
                    is_folder=True,
                    name=path,
                    repo_id=self.id
                )
                el.is_code_file = False
                el.ast = None
                el.extension = None
                if not el.is_hidden():
                    session.add(el)
                    session.commit()
                    session.flush()


class Element(Base):
    __table__ = Base.metadata.tables['element']

    def ignore(self):
        avoid = [None, "", ".md", ".yml", ".sh", ".h"]
        return True if \
            ("readme" in self.name) \
            or ("requirement" in self.name) \
            or ("setup" in self.name) \
            or self.is_hidden() \
            or self.extension in avoid \
            else False

    def is_hidden(self):
        for data in self.name.split("/"):
            if data.startswith("."):
                return True
        return False

    def get_extension(self):
        return os.path.splitext(self.name)[-1]

    def set_is_code_file(self):
        return self.extension == '.py'

    def set_ast(self):
        f = open(self.name, 'r')
        ast = get_ast.make_ast(f.read())
        f.close()
        return ast


class Datasets(Base):
    __table__ = Base.metadata.tables['datasets']

    @classmethod
    def by_repo_name(cls, repo_name):
        return Datasets.query.join(Repo).filter(Repo.name == repo_name).all()

class Commits(Base):
    __table__ = Base.metadata.tables['commits']



# Printing table names
# print(Base.classes.keys())
# Repo = Base.classes.repos


# with open('data/datasetv1.csv') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line = 1
#     for row in csv_reader:
#         repo = Repo(id=int(row[0]),
#                     link=row[1],
#                     nb_commits=row[2],
#                     name=row[1].replace("https://github.com/", ""),
#                     folder_name=row[1].split("/")[-1])
#         session.add(repo)
#         session.commit()
#         print("Added line:", line)
#         line += 1
#         session.flush()
