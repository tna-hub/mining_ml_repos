from sqlalchemy import Integer, Column, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from models import Base

assoc_native_func_param = Table('assoc_native_func_arg', Base.metadata,
                                Column('native_func_id', Integer, ForeignKey('native_func.id')),
                                Column('param_id', Integer, ForeignKey('param.id'))
                                )

assoc_lib_func_param = Table('assoc_lib_func_arg', Base.metadata,
                             Column('lib_func_id', Integer, ForeignKey('lib_func.id')),
                             Column('param_id', Integer, ForeignKey('param.id'))
                             )
assoc_custom_func_param = Table('assoc_custom_func_arg', Base.metadata,
                                Column('custom_func_id', Integer, ForeignKey('custom_func.id')),
                                Column('param_id', Integer, ForeignKey('param.id'))
                                )


class NativeFunc(Base):
    __tablename__ = 'native_func'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Association rule
    params = relationship(
        "Param",
        secondary=assoc_native_func_param)


class Lib(Base):
    __tablename__ = 'lib'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lib_funcs = relationship('LibFunc', backref='lib', lazy='dynamic')


class LibFunc(Base):
    __tablename__ = 'lib_func'
    id = Column(Integer, primary_key=True)
    lib_id = Column(ForeignKey('lib.id'))
    name = Column(String)
    lib_name = Column(String)

    # Association rule
    params = relationship(
        "Param",
        secondary=assoc_lib_func_param)


class CustomFunc(Base):
    __tablename__ = 'custom_func'
    id = Column(Integer, primary_key=True)
    code_id = Column(Integer, ForeignKey('code.id'))
    native_func_called = Column(Integer, ForeignKey('native_func.id'))
    lib_func_called = Column(Integer, ForeignKey('lib_func.id'))
    name = Column(String)
    def_in_file = Column(Integer, ForeignKey('element.id'))

    # Association rule
    params = relationship(
        "Param",
        secondary=assoc_custom_func_param)


class Param(Base):
    __tablename__ = 'param'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    position = Column(Integer)
