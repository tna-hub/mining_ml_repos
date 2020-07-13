import ast

from sqlalchemy import Column, Integer, Text, ForeignKey, JSON, orm
from sqlalchemy.orm import relationship

from models import Base

from models.asts import Call, Import, ImportFrom, ClassDef, Assign, AstObject

nat_lib_names = ['numpy', 'pandas']


class Code(Base, ast.NodeVisitor):
    __tablename__ = 'code'
    id = Column(Integer, primary_key=True)
    content = Column(Text)
    file_id = Column('element', ForeignKey('element.id'))
    json_ast = Column(JSON, comment="json ast of the file's code")
    json_ast = Column(JSON, comment="json ast of the file's code")

    element = relationship('Element', back_populates="code")  # One to One relation with table Element

    # One to Many relations
    import_froms = relationship('ImportFrom', backref='code', lazy='dynamic')
    imports = relationship('Import', backref='code', lazy='dynamic')
    assigns = relationship('Assign', backref='code', lazy='dynamic')
    calls = relationship('Call', backref='code', lazy='dynamic')
    custom_funcs = relationship('CustomFunc', backref='code', lazy='dynamic')
    class_defs = relationship('ClassDef', backref='code', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Code, self).__init__(**kwargs)
        # self.set_mods()

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

    def visit_Assign(self, node):
        if not isinstance(node.value, ast.Name):
            obj = AstObject(node.value)
            ass = Assign(lineno=node.lineno, target=node.targets[0].id if isinstance(node.targets[0], ast.Name) else None, ast_object=obj)
            if ass.target is not None and ass.ast_object.cls is not None:
                self.assigns.append(ass)


'''
    def visit_Import(self, node):
        for imp in node.names:
            self.imports.append(Import(module=imp.name, alias=imp.asname))

    def visit_ImportFrom(self, node):
        for imp in node.names:
            self.import_froms.append(ImportFrom(module=node.module, name=imp.name, alias=imp.asname, level=node.level))


    def visit_Call(self, node):

        self.calls.append(Call(node))

    def visit_ClassDef(self, node):
        self.class_defs.append(ClassDef(node, self.mods))

        # self.class_defs.append

    def visit_FunctionDef(self, node):
        pass
'''
