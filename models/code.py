from sqlalchemy.orm import relationship

from models.asts import Import, ImportFrom, Call, Argument, Assign
from models.gits import Element
from models import Base
import ast
from sqlalchemy import Column, ForeignKey, Integer, JSON, Text


def classname(cls):
    return cls.__class__.__name__


# Code and python ast classes
class Code(ast.NodeVisitor, Base):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    file_id = Column('element', ForeignKey('element.id'))
    json_ast = Column(JSON, comment="json ast of the file's code")

    element = relationship('Element', back_populates="code")  # One to One relation with table Element

    # One to Many relations
    import_froms = relationship('ImportFrom', backref='code', lazy='dynamic')
    imports = relationship('Import', backref='code', lazy='dynamic')
    assigns = relationship('Assign', backref='code', lazy='dynamic')
    calls = relationship('Call', backref='code', lazy='dynamic')
    class_defs = relationship('ClassDef', backref='code', lazy='dynamic')
    function_defs = relationship('FunctionDef', backref='code', lazy='dynamic')

    def visit_Import(self, node):
        for imp in node.names:
            self.imports.append(Import(module=imp.name, alias=imp.asname))

    def visit_ImportFrom(self, node):
        for imp in node.names:
            self.import_froms.append(ImportFrom(module=node.module, name=imp.name, alias=imp.asname, level=node.level))

    def visit_Call(self, node):
        call = Call()
        if hasattr(node.func, 'attr'):
            call.name = node.func.attr
            if isinstance(node.func.value, ast.Name):
                call.attr = node.func.value.id
        elif hasattr(node.func, 'id'):
            call.name = node.func.id
        if hasattr(node, 'args'):
            i = 0
            for arg in node.args:
                if isinstance(arg, ast.Constant):
                    call.arguments.append(Argument(lineno=node.lineno, cls='Str', position=i, value=str(arg.value)))
                elif isinstance(arg, ast.Name):
                    var = Argument(lineno=node.lineno,
                                   cls='Var',
                                   position=i,
                                   value=None,
                                   var_name=arg.id)
                    # var_value = var.get_var_value(node.lineno, arg.id) TODO
                    #var.value = var_value
                    call.arguments.append(var)
                elif isinstance(arg, ast.BinOp):
                    if isinstance(arg.op, ast.Add):
                        binop = Argument(lineno=node.lineno, cls='BinOp', position=i, value=None)
                        ars = binop.get_binop_constants(arg, [])
                        if ars is not None:
                            for ar in ars:
                                binop.value += ar
                            call.arguments.append(binop)
                i = i + 1
        if hasattr(node, 'keywords'):
            for keyword in node.keywords:
                if hasattr(keyword, 'arg') and hasattr(keyword, 'value'):
                    if isinstance(keyword.value, ast.Constant):
                        call.arguments.append(Argument(lineno=node.lineno,
                                                       cls='Str',
                                                       position=keyword.arg, value=str(keyword.value.value)))
                    elif isinstance(keyword.value, ast.Name):
                        var = Argument(lineno=node.lineno,
                                       cls='Var',
                                       position=keyword.arg,
                                       value=None,
                                       var_name=keyword.value.id)
                        # var_value = var.get_var_value(node.lineno, var.var_name) TODO
                        # var.value = var_value
                        call.arguments.append(var)
                    elif isinstance(keyword.value, ast.BinOp):
                        if isinstance(keyword.value.op, ast.Add):
                            binop = Argument(lineno=node.lineno, cls='BinOp', position=keyword.arg, value=None)
                            ars = binop.get_binop_constants(keyword.value, [])
                            if ars is not None:
                                for ar in ars:
                                    binop.value += ar
                                call.arguments.append(binop)

    def visit_Assign(self, node):
        if hasattr(node, 'targets') and hasattr(node, 'value'):
            if isinstance(node.targets[0], ast.Name):
                if isinstance(node.value, ast.Constant):
                    ass = Assign(lineno=node.lineno,
                                 var_name=node.targets[0].id,
                                 value=str(node.value.value))
                    self.assigns.append(ass)
                elif isinstance(node.value, ast.Name):
                    ass = Assign(lineno=node.lineno,
                                 var_name=node.targets[0].id,
                                 refers_to=node.value.id)
                    self.assigns.append(ass)
                elif isinstance(node.value, ast.BinOp):
                    if isinstance(node.value.op, ast.Add):
                        binop = Assign(lineno=node.lineno, var_name=node.targets[0].id, value=None)
                        ars = binop.get_binop_constants(node.value, [])
                        if ars is not None:
                            for ar in ars:
                                binop.value += str(ar)
                            self.assigns.append(binop)


    def get_arg_var_value(self, arglineno, var_name):
        for var in reversed(self.assigns):
            if var.lineno > arglineno:
                for key in var.keys():
                    if key == var_name:
                        return var[key]
