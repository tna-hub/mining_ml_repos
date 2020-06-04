import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# Using automap extension
from sqlalchemy.ext.automap import automap_base
from git import Repo as rp

import from_github
import get_ast
from pydriller import RepositoryMining as rpm
import configparser

config = configparser.ConfigParser()
config.read('data/config.ini')

host = config['postgresql']['host']
user = config['postgresql']['user']
passwd = config['postgresql']['passwd']
db = config['postgresql']['db']

engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(user,
                                                                  passwd,
                                                                  host,
                                                                  db))
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
                rp.clone_from(self.link.replace('://', '://:@'), self.folder_name)
            return True
        except Exception as e:
            return False

    @classmethod
    def get_elements(cls):
        return session.query(Element).filter(Element.repo_id == Repo.id).all()

    def extract_elements(self):
        for r, d, f in os.walk(self.folder_name):
            for file in f:
                path = os.path.join(r, file)
                print('        +Found file:', path)
                el = Element(
                    is_folder=False,
                    name=path,
                    repo_id=self.id
                )
                el.extension = el.get_extension()
                el.is_code_file = el.set_is_code_file()
                if el.is_code_file:
                    el.ast, el.imports = el.set_ast_and_modules()
                if not el.ignore():
                    session.add(el)
                    session.commit()
                    session.flush()

            for folder in d:
                path = os.path.join(r, folder)
                print('        +Found folder:', path)
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
            print('        +Getting commit:', commit.hash)
            com = Commit()
            com2 = from_github.get_commit(self.name, commit.hash)
            stats = com2.stats if com2 is not None else None
            total = stats.total if stats is not None else None
            data = {
                'repo_id': self.id,
                'sha': commit.hash,
                'commit_date': commit.committer_date,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'total_modifs': total
            }
            com.set_data(data)
            session.add(com)
            session.commit()
            session.flush()

            if com2 is not None:
                for mod in com2.files:
                    old_path = mod.previous_filename
                    new_path = mod.filename
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
                                'change_type': mod.status,
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

    def set_ast_and_modules(self):
        try:
            f = open(self.name, 'r')
            code = f.read()
            ast = get_ast.make_ast(code)
            imports = get_ast.get_modules(code)
            f.close()
        except Exception as e:
            ast = {'error': "{}".format(e)}
            imports = None
        return ast, imports


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
        self.total_modifs= data['total_modifs']


    @classmethod
    def by_sha(cls, sha):
        return session.query(Commit).filter(Commit.sha == sha)


class Commit_mod(Base):
    __table__ = Base.metadata.tables['commit_modifications']

    def set_data(self, data):
        self.file_id = data['file_id']
        self.change_type = data['change_type']
        self.commit_id = data['commit_id']
