import ast

import astor
from sqlalchemy import Column, Integer, Text, ForeignKey, JSON, orm
from sqlalchemy.orm import relationship

from models import Base

from models.asts import Call, Import, ClassDef, Assign, AstObject
from models.func_load_files import s_funcs
from copy import deepcopy as dc


def classname(cls):
    return cls.__class__.__name__


stat = {}


class Code(Base, ast.NodeVisitor):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    file_id = Column('element', ForeignKey('element.id'))
    json_ast = Column(JSON, comment="json ast of the file's code")
    tot = 0
    element = relationship('Element', back_populates="code")  # One to One relation with table Element

    # One to Many relations
    imports = relationship('Import', backref='code', lazy='dynamic')
    assigns = relationship('Assign', backref='code', lazy='dynamic')
    calls = relationship('Call', backref='code', lazy='dynamic')
    custom_funcs = relationship('CustomFunc', backref='code', lazy='dynamic')
    class_defs = relationship('ClassDef', backref='code', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Code, self).__init__(**kwargs)
        self.tot = 0
        self.s_funcs = None
        self.imp_funcs = []
        self.imps = []

    def start(self):
        self.s_funcs = dc(s_funcs)
        libchanges = {}
        fchanges = {}
        if self.imports is not None:
            for imp in self.imports:
                real_lib = real_func = None
                alias = imp.alias
                mods = imp.module.split('.')
                if len(mods) > 1:
                    real_lib = mods[0]
                    real_func = mods[-1]
                elif len(mods) == 1:
                    real_lib = mods[0]
                    real_func = None
                if real_lib is not None and real_func is None:
                    if real_lib in s_funcs.keys():
                        alias_lib = libchanges[real_lib] if real_lib in libchanges.keys() else real_lib
                        if alias is not None:
                            self.s_funcs[alias] = self.s_funcs.pop(alias_lib)
                            libchanges[real_lib] = alias
                        else:
                            self.s_funcs[real_lib] = self.s_funcs.pop(alias_lib)
                            del libchanges[real_lib]
                elif real_lib is not None and real_func is not None:
                    if real_lib in s_funcs.keys():
                        alias_lib = libchanges[real_lib] if real_lib in libchanges.keys() else real_lib
                        lib_funcs = s_funcs[real_lib]
                        if real_func in lib_funcs.keys():
                            alias_func = fchanges[real_func] if real_func in fchanges.keys() else real_func
                            if alias is not None:
                                self.s_funcs[alias_lib][alias] = self.s_funcs[alias_lib].pop(alias_func)
                                fchanges[real_func] = alias
                            else:
                                self.s_funcs[alias_lib][real_func] = self.s_funcs[alias_lib].pop(alias_func)
                                del fchanges[real_func]


        libs = [imp.mdule.split('.')[0] for imp in self.imports]
        for imp in self.imports:
            if len(imp.module.split('.')) == 1:
                self.imps.append(imp.module)
            else:
                self.imp_funcs.append(imp.module.split('.')[-1])

        for lib, funcs in self.s_funcs:



        # self.set_mods()

    '''
        @orm.reconstructor
        def set_mods(self):
            uniq_imports = {}
            for imp in self.imports:
                uniq_imports[imp.module] = imp.alias
            for imp in self.import_froms:
                uniq_imports['{}.{}'.format(imp.module, imp.name)] = imp.alias
            # First, to identify custom funcs, Remove all imports not matching a known (native or lib) function
            self.all_mods = [mod for mod in uniq_imports.keys()]
            self.mods = []
            for mod in self.all_mods:
                sp = mod.split('.')
                if sp[0] in nat_lib_names:
                    self.mods.append(mod)
    '''

    def visit_Call(self, node):
        try:
            name = None
            attr = None
            arg = None
            if hasattr(node.func, 'attr'):
                name = node.func.attr
                if isinstance(node.func.value, ast.Name):
                    attr = node.func.value.id
            elif hasattr(node.func, 'id'):
                name = node.func.id


            if hasattr(node, 'args'):
                if len(node.args) > 0:
                    mvalue = None
                    if len(node.args) == 1:
                        for lib, funcs in self.s_funcs:
                            if name in funcs.keys():
                                mvalue = funcs[name]['set_mode_from_name']
                                break
                        mvalue = mvalue if mvalue is not None else 'r'
                        mode = ast.Constant(value=mvalue)
                        file = node.args[0]
                    else:
                        file = node.args[1] if 'torch' in self.imps or 'tensorflow' in self.imps else node.args[0]
                        for lib, funcs in self.s_funcs:
                            if name in funcs.keys():
                                mvalue = funcs[name]['set_mode_from_name']
                                break
                        mode = node.args[2]
            if hasattr(node, 'keywords'):
                mvalue = 'r'
                if len(node.keywords) > 0:
                    if len(node.keywords) == 1:
                        for lib, funcs in self.s_funcs:
                            if name in funcs.keys():
                                mvalue = funcs[name]['set_mode_from_name']
                        mode = ast.Constant(value='r')
                        file = node.args[0]
                    else:
                        for keyword in node.keywords:
                            if keyword.arg == 'mode':
                                arg = keyword.value

            if name is not None and name in funcs and arg is not None:
                self.tot += 1
                cls = classname(arg)
                if cls in stat.keys():
                    stat[cls] += 1
                else:
                    stat[cls] = 1
        except Exception as e:
            print(e)

    def visit_Import(self, node):
        for imp in node.names:
            self.imports.append(Import(module=imp.name, alias=imp.asname))

    def visit_ImportFrom(self, node):
        for imp in node.names:
            self.imports.append(Import(module=str(node.module)+'.'+str(imp.name), alias=imp.asname))


"""
    def visit_ClassDef(self, node):
        cl =ClassDef(node, [])
        for call in cl.calls:
            if call.name == 'open':
                print('Yes found function open in classdef', cl.name, 'at lineno', call.lineno)
                print(astor.to_source(node, indent_with=' ' * 4, add_line_information=False))
            self.class_defs.append(ClassDef(node, []))

        # self.class_defs.append

    def visit_FunctionDef(self, node):
        pass
"""
"""
    def visit_Assign(self, node):
        if isinstance(node.value, (ast.Constant, ast.BinOp)):
            obj = AstObject(node.value)
            ass = Assign(lineno=node.lineno, target=node.targets[0].id if isinstance(node.targets[0], ast.Name) else None, ast_object=obj)
            if ass.target is not None and ass.ast_object.cls is not None and ass.ast_object.value is not None:
                self.assigns.append(ass)



    def visit_Import(self, node):
        for imp in node.names:
            self.imports.append(Import(module=imp.name, alias=imp.asname))

    def visit_ImportFrom(self, node):
        for imp in node.names:
            self.import_froms.append(ImportFrom(module=node.module, name=imp.name, alias=imp.asname, level=node.level))


    def visit_Call(self, node):

        self.calls.append(Call(node))
"""
