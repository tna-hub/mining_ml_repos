import ast
import re

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models import Base
from models.func_load_files import CustomFunc



def classname(cls):
    return cls.__class__.__name__


class Call(Base):
    __tablename__ = 'call'
    id = Column(Integer, primary_key=True)
    code_id = Column(Integer, ForeignKey('code.id'))
    arguments = relationship('Argument', backref='call', lazy='dynamic')
    attr = Column(String)
    name = Column(String)
    lineno = Column(Integer)

    def __init__(self, node=None, **kwargs):
        super(Call, self).__init__(**kwargs)
        self.lineno = node.lineno
        if hasattr(node.func, 'attr'):
            self.name = node.func.attr
            if isinstance(node.func.value, ast.Name):
                self.attr = node.func.value.id
        elif hasattr(node.func, 'id'):
            self.name = node.func.id
        if hasattr(node, 'args'):
            i = 0
            for arg in node.args:
                if isinstance(arg, (ast.Constant, ast.Name, ast.BinOp, ast.Attribute)):
                    if isinstance(arg, ast.Attribute):
                        if isinstance(arg.value, ast.Name):
                            if arg.value.id == 'self':
                                arg = ast.Name(id=arg.attr, ctx='Load')
                    self.arguments.append(Argument(position=i, ast_object=AstObject(arg)))
                i = i + 1
        if hasattr(node, 'keywords'):
            for keyword in node.keywords:
                if hasattr(keyword, 'arg') and hasattr(keyword, 'value'):
                    arg = keyword.value
                    if isinstance(arg, (ast.Constant, ast.Name, ast.BinOp, ast.Attribute)):
                        if isinstance(arg, ast.Attribute):
                            if isinstance(arg.value, ast.Name):
                                if arg.value.id == 'self':
                                    arg = ast.Name(id=arg.attr, ctx='Load')
                        self.arguments.append(Argument(position=keyword.arg, ast_object=AstObject(arg)))

class Import(Base):
    __tablename__ = 'import'
    id = Column(Integer, primary_key=True)
    module = Column(String)
    alias = Column(String)
    code_id = Column(Integer, ForeignKey('code.id'))


class Assign(Base):
    __tablename__ = 'assign'
    id = Column(Integer, primary_key=True)
    code_id = Column(ForeignKey('code.id'))
    target = Column(String)
    lineno = Column(Integer)
    ast_object_id = Column(ForeignKey('ast_object.id'))
    ast_object = relationship('AstObject', uselist=False, back_populates="assign")


class Argument(Base):
    __tablename__ = 'arg'
    id = Column(Integer, primary_key=True)
    call_id = Column(Integer, ForeignKey('call.id'))
    position = Column(String)
    ast_object_id = Column('ast_object', ForeignKey('ast_object.id'))
    ast_object = relationship('AstObject', uselist=False, back_populates="arg")


class AstObject(Base):
    __tablename__ = 'ast_object'
    id = Column(Integer, primary_key=True)
    arg = relationship('Argument', back_populates="ast_object")  # One to One relation with table Argument
    assign = relationship('Assign', back_populates="ast_object")  # One to One relation with table Assign
    value = Column(String)
    cls = Column(String)
    var_name = Column(String)

    def __init__(self, node=None, **kwargs):
        super(AstObject, self).__init__(**kwargs)
        self.cls = classname(node) if isinstance(node, (ast.Name, ast.Constant, ast.BinOp)) else None
        if self.cls == 'Name':
            self.var_name = node.id
        elif self.cls == 'Constant':
            try:
                self.value = str(node.value).replace('\x00', '').encode("utf-8", errors="ignore").decode()
            except Exception as e:
                self.value = None
        elif self.cls == 'BinOp' and self.value is None:
            if isinstance(node.op, ast.Add):
                constants = set_constants(node, constants=[])
                val = self.set_binop_value(constants)
                self.value = str(val).replace('\x00', '').encode("utf-8",
                                                                 errors="ignore").decode() if val is not None else None

    def set_binop_value(self, constants):
        if constants is not None:
            value = ''
            for val in reversed(constants):
                value += val
            return value
        else:
            return None


def set_constants(node, constants):
    lhs = node.left
    rhs = node.right
    if isinstance(node.op, ast.Add) and constants is not None:
        if isinstance(rhs, ast.Constant):
            constants.append(str(rhs.value))
        else:
            constants = None
        if isinstance(lhs, ast.Constant) and constants is not None:
            constants.append(str(lhs.value))
        elif isinstance(lhs, ast.BinOp) and constants is not None:
            set_constants(node=lhs, constants=constants)
        else:
            constants = None
    return constants


class ClassDef(Base, ast.NodeVisitor):
    __tablename__ = 'class_def'
    id = Column(Integer, primary_key=True)
    code_id = Column(ForeignKey('code.id'))
    name = Column(String)
    is_custom_func_load_files = False

    def __init__(self, node=None, **kwargs):
        super(ClassDef, self).__init__(**kwargs)
        self.name = node.name
        self.lineno = node.lineno
        self.calls = []
        self.params = []
        if node is not None:
            args = node.args.args
            if len(args) > 0:
                self.params = [arg.arg for arg in args]
                self.params = [arg.arg for arg in args]
        self.visit(node)

    def visit_FunctionDef(self, node):
        fd = FunctionDef(node)
        if fd.name == '__init__':
            fd.visit(node)
            self.params = fd.params
            self.calls = fd.calls


class FunctionDef(ast.NodeVisitor):
    def __init__(self, node, mods=None):
        self.mods = mods
        self.calls = []
        self.params = []
        self.name = node.name
        self.lineno = node.lineno
        for arg in node.args.args:
            if arg.arg != 'self':
                self.params.append(arg.arg)

    def get_nat_or_lib_funcs(self, call, mods):
        print(call.name)
        print(mods)
        if call.attr is None:
            for key, value in mods.items():
                if (call.name == key.split('.')[-1] and value is None) or (call.name == value and value is not None):
                    return True, call
        else:
            for key, value in mods.items():
                if (call.attr == key.split('.')[-1] and value is None) or (call.attr == value and value is not None):
                    return True, call
        return False, None

    def visit_Call(self, node):
        # res, call = self.get_nat_or_lib_funcs(Call(node=node), self.mods)
        call = Call(node=node)
        if call.name == 'open':
            self.calls.append(call)
