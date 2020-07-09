import os
from git import Repo as rp
from pydriller import RepositoryMining as rpm

from sqlalchemy.orm import relationship

from models import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table

from models.code import Code

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

    def download(self):
        try:
            if not os.path.isdir(self.folder_name):
                rp.clone_from(self.link.replace('://', '://:@'), self.folder_name)
            return True
        except Exception as e:
            return False

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
                if el.ignore():
                    if el.is_code_file:
                        el.set_code()
                    self.elements.append(el)

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
                    self.elements.append(el)

    def set_commits(self):
        for commit in rpm(self.folder_name).traverse_commits():
            com = Commit()
            data = {
                'repo_id': self.id,
                'sha': commit.hash,
                'commit_date': commit.committer_date,
                'author_name': commit.author.name,
                'author_email': commit.author.email,
                'total_modifs': 0
            }
            com.set_data(data)
            total = 0
            for mod in commit.modifications:
                total += abs(mod.added) + abs(mod.removed)
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
                        com_mod = CommitModification()
                        com_mod.set_data(data)
                        com.commit_modifications.append(com_mod)
                        # session.flush()
            com.total_modifs = total
            self.commits.append(com)


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
    def_func_load_files = relationship('CustomFunc')

    commit_modifications = relationship('CommitModification', back_populates="file")
    load_files = relationship(
        "Dataset",
        secondary=assoc_file_dataset,
        back_populates="loaded_in")

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

    def set_code(self):
        try:
            with open(self.name, 'r') as f:
                code = f.read()
                self.code = Code(content=code)
        except Exception as e:
            ast = {'error': "{}".format(e)}
            self.code = None
            self.json_ast = ast


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
