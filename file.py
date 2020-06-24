# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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

    id = Column(Integer, primary_key=True, server_default=text("nextval('commits_id_seq1'::regclass)"))
    repo_id = Column(Integer, ForeignKey('repo.id'), nullable=False)
    sha = Column(String, nullable=False)
    commit_date = Column(DateTime)
    author_name = Column(String)
    author_email = Column(String)
    total_modifs = Column(Integer)
    commit_modifications = relationship('CommitModifications', backref='commit', lazy='dynamic')


class Element(Base):
    __tablename__ = 'element'
    __table_args__ = {'comment': 'Information of files and folders in the repositories'}

    id = Column(Integer, primary_key=True)
    name = Column(String(500))
    is_code_file = Column(Boolean, comment='Set to True or False if file has code or not')
    code = relationship("Code", uselist=False, back_populates="element")
    repo_id = Column(ForeignKey('repos.id'))
    is_folder = Column(Boolean, nullable=False, comment='True if it is a folder, false if it is not')
    extension = Column(String)

    repo = relationship('Repo')


class CommitModification(Base):
    __tablename__ = 'commit_modifications'

    id = Column(Integer, primary_key=True, server_default=text("nextval('commit_modifications_id_seq1'::regclass)"))
    file_id = Column(ForeignKey('element.id'), nullable=False)
    change_type = Column(String)
    commit_id = Column(ForeignKey('commits.id'))

    commit = relationship('Commit')
    file = relationship('Element')


class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, server_default=text("nextval('datasets_id_seq'::regclass)"))
    element_id = Column(ForeignKey('element.id'), nullable=False)
    heuristic = Column(String(2), nullable=False, comment='The heuristic used to identify as dataset')
    file_mention = Column(ForeignKey('element.id'), nullable=False, comment='The file where the dataset is loaded')
    repo_id = Column(ForeignKey('repos.id'), nullable=False)

    element = relationship('Element', primaryjoin='Dataset.element_id == Element.id')
    element1 = relationship('Element', primaryjoin='Dataset.file_mention == Element.id')
    repo = relationship('Repo')
