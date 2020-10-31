from sqlalchemy.orm import relationship

from models import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table

assoc_file_dataset = Table('assoc_file_dataset', Base.metadata,
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

    def set_datafiles(self):
        # TODO
        return

    def get_code_files(self):
        for el in self.elements:
            if el.is_code_file:
                yield el

    def get_non_code_files(self):
        for el in self.elements:
            if not el.is_code_file:
                yield el


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
    file_id = Column(Integer, ForeignKey('element.id'), nullable=False)

    commit = relationship("Commit", back_populates="commit_modifications")
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
    name = Column(String)
    element_id = Column(ForeignKey('element.id'))
    heuristic = Column(String(2), nullable=False, comment='The heuristic used to identify as dataset')
    repo_id = Column(ForeignKey('repo.id'), nullable=False)
    loaded_in = relationship(
        "Element",
        secondary=assoc_file_dataset,
        back_populates="load_files")
