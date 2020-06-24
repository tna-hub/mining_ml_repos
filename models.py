from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship

Base = declarative_base()

# Code and python ast classes
class Code(Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    element_id = relationship("Element", back_populates="code")
    json_ast = Column(JSON, comment="json ast of the file's code")
    importfroms = relationship('ImportFrom', backref='code', lazy='dynamic')
    imports = relationship('Import', backref='code', lazy='dynamic')
    assigns = relationship('Assign', backref='code', lazy='dynamic')
    calls = relationship('Call', backref='code', lazy='dynamic')
    classdefs = relationship('ClassDef', backref='code', lazy='dynamic')
    functiondefs = relationship('FunctionDef', backref='code', lazy='dynamic')
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
    lineno = Column(Integer)
    # TODO


class Str(Base):
    __tablename__ = 'str'
    lineno = Column(Integer)
    # TODO
