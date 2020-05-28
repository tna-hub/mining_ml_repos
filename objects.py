import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Using automap extension
from sqlalchemy.ext.automap import automap_base
from git import Repo as rp

import get_ast
from pydriller import RepositoryMining as rpm


engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost/ml_repos')
Base = automap_base()
Base.prepare(engine, reflect=True)
session = scoped_session(sessionmaker(bind=engine))


class Repo(Base):
    __table__ = Base.metadata.tables['repos']

    @classmethod
    def save(cls):
        return session.add(Repo)

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

    def set_commits(self):
        for commit in rpm(self.folder_name).traverse_commits():
            com = Commit()
            data = {
                'repo_id': self.id,
                'sha': commit.hash,
                'commit_date': commit.committer_date,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
            }
            com.set_data(data)
            session.add(com)
            session.commit()
            session.flush()

            for mod in commit.modifications:
                old_path = mod.old_path
                new_path = mod.new_path
                if old_path is None:
                    path = new_path
                elif new_path is None:
                    path = old_path
                elif old_path == new_path:
                    path = old_path
                else:
                    path = None
                if path is not None:
                    path = "{}/{}".format(self.folder_name, path)
                    file = Element.by_name_and_repo_id(path, self.id)
                    if file is not None:
                        data = {
                            'file_id': file.id,
                            'change_type': mod.change_type.name,
                            'additions': mod.added,
                            'deletions': mod.removed,
                            'old_path': old_path,
                            'new_path': new_path,
                            'commit_id': com.id
                        }
                        com_mod = Commit_mod()
                        com_mod.set_data(data)
                        session.add(com_mod)
                        session.commit()
                        session.flush()

    @classmethod
    def get_commits(cls):
        return session.query(Commit).filter(Commit.repo_id == Repo.id).all()


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

    @classmethod
    def by_name_and_repo_id(cls, name, repo_id):
        return session.query(Element).filter(Element.name == name).filter(Element.repo_id == repo_id).first()


class Datasets(Base):
    __table__ = Base.metadata.tables['datasets']

    @classmethod
    def by_repo_name(cls, repo_name):
        return Datasets.query.join(Repo).filter(Repo.name == repo_name).all()


class Commit(Base):
    __table__ = Base.metadata.tables['commits']

    def set_data(self, data):
        self.repo_id = data['repo_id']
        self.sha = data['sha']
        self.commit_date = data['commit_date']
        self.author_name = data['author_name']
        self.author_email = data['author_email']


    @classmethod
    def by_sha(cls, sha):
        return session.query(Commit).filter(Commit.sha == sha)


class Commit_mod(Base):
    __table__ = Base.metadata.tables['commit_modifications']

    def set_data(self, data):
        self.file_id = data['file_id']
        self.change_type = data['change_type']
        self.additions = data['additions']
        self.deletions = data['deletions']
        self.old_path = data['old_path']
        self.new_path = data['new_path']
        self.commit_id = data['commit_id']

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
