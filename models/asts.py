import ast

from sqlalchemy.orm import relationship

from models import Base
from sqlalchemy import Column, ForeignKey, Integer, String, JSON


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
    code_id = Column(Integer, ForeignKey('code.id'))
    var_name = Column(String)
    refers_to = Column(String)
    value = Column(String)
    binop = relationship("BinOp", uselist=False, back_populates="assign")



class BinOp(Base):
    __tablename__ = 'binop'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    value = Column(String)
    arg_id = Column(Integer, ForeignKey('arg.id'))
    assign_id = Column(Integer, ForeignKey('assign.id'))
    constants = relationship('Constant', backref='binop', lazy='dynamic')
    arg = relationship('Argument', back_populates="binop")
    assign = relationship('Assign', back_populates="binop")


    def set_constants(self, node, position=-1):
        lhs = node.left
        rhs = node.right
        if isinstance(node.op, ast.Add):
            if isinstance(rhs, ast.Constant):
                position += 1
                const = Constant(cls='Str', value=rhs.value, position=position)
                self.constants.append(const)
            elif isinstance(rhs, ast.Name):
                # value = self.get_var_value(node.lineno, rhs.id)
                position += 1
                const = Constant(cls='Var', var_name=rhs.id, position=position)
                self.constants.append(const)
            if isinstance(lhs, ast.Constant):
                position += 1
                const = Constant(cls='Str', value=lhs.value, position=position)
                self.constants.append(const)
            elif isinstance(lhs, ast.Name):
                # value = self.get_var_value(node.lineno, rhs.id)
                position += 1
                const = Constant(cls='Var', var_name=rhs.id, position=position)
                self.constants.append(const)
            elif isinstance(lhs, ast.BinOp):
                self.set_constants(node=lhs, position=position)


class Constant(Base):
    __tablename__ = 'constant'
    id = Column(Integer, primary_key=True)
    binop_id = Column(Integer, ForeignKey('binop.id'))
    var_name = Column(String)
    cls = Column(String)
    value = Column(String)
    position = Column(Integer)


class Call(Base):
    __tablename__ = 'call'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    code_id = Column(Integer, ForeignKey('code.id'))
    arguments = relationship('Argument', backref='call', lazy='dynamic')
    attr = Column(String)
    name = Column(String)


class ClassDef(Base):
    __tablename__ = 'class_def'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    code_id = Column(Integer, ForeignKey('code.id'))
    # TODO


class FunctionDef(Base):
    __tablename__ = 'function_def'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    code_id = Column(Integer, ForeignKey('code.id'))
    # TODO


class Argument(Base):
    __tablename__ = 'arg'
    id = Column(Integer, primary_key=True)
    lineno = Column(Integer)
    code_id = Column(Integer, ForeignKey('code.id'))
    call_id = Column(Integer, ForeignKey('call.id'))
    cls = Column(String)
    position = Column(String)
    value = Column(String)
    var_name = Column(String)
    binop = relationship("BinOp", uselist=False, back_populates="arg")
