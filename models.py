from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, Table
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
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
                                                                  db), echo=True)


Base = declarative_base()
metadata = Base.metadata

assoc_file_dataset = Table('assoc_file_dataset', metadata,
                           Column('dataset_id', Integer, ForeignKey('dataset.id')),
                           Column('loaded_in', Integer, ForeignKey('element.id'))
                           )

# Git classes

class Repo(Base):
    __tablename__ = 'repo'
    __table_args__ = {'comment': 'Repositories to analyse'}

    id = Column(Integer, primary_key=True)
    link = Column(String(5000), nullable=False, comment='Github link')
    nb_commits = Column(Integer, comment='Total commits in the repository')
    name = Column(String(500))
    folder_name = Column(String(500))
    commits = relationship('Commit', backref='repo', lazy='dynamic')
    elements = relationship('Element', backref='repo', lazy='dynamic')


class Commit(Base):
    __tablename__ = 'commit'

    id = Column(Integer, primary_key=True)
    repo_id = Column(Integer, ForeignKey('repo.id'), nullable=False)
    sha = Column(String, nullable=False)
    commit_date = Column(DateTime)
    author_name = Column(String)
    author_email = Column(String)
    total_modifs = Column(Integer)
    commit_modifications = relationship('CommitModification', back_populates="commit")


class CommitModification(Base):
    __tablename__ = 'commit_modification'

    id = Column(Integer, primary_key=True, )
    change_type = Column(String)
    commit_id = Column(Integer, ForeignKey('commit.id'))
    commit = relationship("Commit", back_populates="commit_modifications")
    file_id = Column(Integer, ForeignKey('element.id'), nullable=False)
    file = relationship("Element", back_populates="commit_modifications")


class Element(Base):
    __tablename__ = 'element'
    __table_args__ = {'comment': 'Information of files and folders in the repositories'}

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    is_code_file = Column(Boolean, comment='Set to True or False if file has code or not')
    repo_id = Column(Integer, ForeignKey('repo.id'))
    is_folder = Column(Boolean, nullable=False, comment='True if it is a folder, false if it is not')
    extension = Column(String)

    code = relationship("Code", uselist=False, back_populates="element")

    commit_modifications = relationship('CommitModification', back_populates="file")
    load_files = relationship(
        "Dataset",
        secondary=assoc_file_dataset,
        back_populates="loaded_in")


class Dataset(Base):
    __tablename__ = 'dataset'

    id = Column(Integer, primary_key=True)
    element_id = Column(ForeignKey('element.id'), nullable=False)
    heuristic = Column(String(2), nullable=False, comment='The heuristic used to identify as dataset')
    repo_id = Column(ForeignKey('repo.id'), nullable=False)
    loaded_in = relationship(
        "Element",
        secondary=assoc_file_dataset,
        back_populates="load_files")




# Code and python ast classes
class Code(Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    file_id = Column('Element', ForeignKey('element.id'))
    json_ast = Column(JSON, comment="json ast of the file's code")

    file = relationship('Element', back_populates="code")  # One to One relation with table Element

    # One to Many relations
    import_froms = relationship('ImportFrom', backref='code', lazy='dynamic')
    imports = relationship('Import', backref='code', lazy='dynamic')
    assigns = relationship('Assign', backref='code', lazy='dynamic')
    calls = relationship('Call', backref='code', lazy='dynamic')
    class_defs = relationship('ClassDef', backref='code', lazy='dynamic')
    function_defs = relationship('FunctionDef', backref='code', lazy='dynamic')
    strs = relationship('Str', backref='code', lazy='dynamic')


class ImportFrom(Base):
    __tablename__ = 'import_from'
    id = Column(Integer, primary_key=True)
    module = Column(String)
    name = Column(String)
    alias = Column(String)
    level = Column(Integer)
    code_id = Column(Integer, ForeignKey('code.id'))


class Import(Base):
    __tablename__ = 'import'
    id = Column(Integer, primary_key=True)
    module = Column(String)
    alias = Column(String)
    code_id = Column(Integer, ForeignKey('code.id'))


class Assign(Base):
    __tablename__ = 'assign'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    # TODO


class Call(Base):
    __tablename__ = 'call'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    # TODO


class ClassDef(Base):
    __tablename__ = 'class_def'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    # TODO


class FunctionDef(Base):
    __tablename__ = 'function_def'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    # TODO


class Str(Base):
    __tablename__ = 'str'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    # TODO

if __name__ == '__main__':
    Base.metadata.create_all(engine)