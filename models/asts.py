import ast

from sqlalchemy.orm import relationship

from models import Base
from sqlalchemy import Column, ForeignKey, Integer, String


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


    def get_binop_constants(self, node, args):
        lhs = node.left
        rhs = node.right
        if isinstance(node.op, ast.Add):
            if isinstance(rhs, ast.Constant):
                args.insert(0, rhs.value)
            elif isinstance(rhs, ast.Name):
                # value = self.get_var_value(node.lineno, rhs.id)
                value = None
                if value is not None:
                    args.insert(0, value)
            else:
                args = None
                return args
            if isinstance(lhs, ast.Constant):
                args.insert(0, lhs.value)
            elif isinstance(lhs, ast.Name):
                # value = self.get_var_value(node.lineno, rhs.id)
                value = None
                if value is not None:
                    args.insert(0, value)
            elif isinstance(lhs, ast.BinOp):
                self.get_binop_constants(lhs, args)
            else:
                args = None
                return args
        else:
            args = None
        return args

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

    def get_binop_constants(self, node, args):
        lhs = node.left
        rhs = node.right
        if isinstance(node.op, ast.Add):
            if isinstance(rhs, ast.Constant):
                args.insert(0, rhs.value)
            elif isinstance(rhs, ast.Name):
                #value = self.get_var_value(node.lineno, rhs.id)
                value = None
                if value is not None:
                    args.insert(0, value)
            else:
                args = None
                return args
            if isinstance(lhs, ast.Constant):
                args.insert(0, lhs.value)
            elif isinstance(lhs, ast.Name):
                # value = self.get_var_value(node.lineno, rhs.id)
                value = None
                if value is not None:
                    args.insert(0, value)
            elif isinstance(lhs, ast.BinOp):
                self.get_binop_constants(lhs, args)
            else:
                args = None
                return args
        else:
            args = None
        return args

    def get_var_value(self, lineno, var_name):
        # TODO
        return ''


