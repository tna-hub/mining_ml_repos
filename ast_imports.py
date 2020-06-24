import inspect
import importlib
import ast


class Imports(ast.NodeVisitor):
    def visit_Import(self, node):
        #print("In Import")
        for imp in node.names:
            #if imp.asname is not None:
                #return imp.name, imp.asname
            print("module name = {}, alias = {}".format(imp.name, imp.asname))
            #else:
                #return imp.name, None
                #print("module name = {}".format(imp.name))
        print()

    def visit_ImportFrom(self, node):
        print("In ImportFrom")
        for imp in node.names:
            if imp.asname is not None:
                print("module = {}\nname = {}\nalias = {}\nlevel = {}\n".
                      format(node.module, imp.name, imp.asname, node.level))
                print(node.lineno)
            else:
                print("module = {}\nname = {}\nlevel = {}\n".
                      format(node.module, imp.name, node.level))
        print()

mod = '''from bisect import bisect_left as bs
import datetime
import time
import numpy as np
from pandas.arrays import hello as b
def foo():
    from re import findall
class Foo():
    def test(self):
        from re import compile as cp, finditer as ft'''
#mod = importlib.import_module(mod)
p = ast.parse(mod)
Imports().visit(p)