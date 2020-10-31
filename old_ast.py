import inspect
import importlib
import ast

#from models import Call


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

import ast

import get_ast
import pprint
#from pattern import ShowStrings

class binop(ast.NodeVisitor):
    def visit_BinOp(self, node):
        a = 'first assign'
        b = a
        c = a + b
        cons = get_binop_contants(node, [])
        if cons is not None:
            res = ''
            for con in cons:
                res += str(con)
            print('result', res)

def test_json_ast(a='hello'):
    hell = 'test'
    #filename = 'mzeageththt'
    filename = 'old_ast.py'
    with open(file='old_ast.py', mode='r') as f:
        #filename = 'hello'
        ast_python = get_ast.code_ast("'test_str_value' + 'test_str_value'")
        node = ast.parse("'test_str_value' + 'test_str_value'")
        b = binop()
        b.visit(node)
        node.lineno = 12
        #print(hell)
        #print(ast_python.json_ast)
        res = get_ast.flatten_json(ast_python.json_ast)
        pprint.pprint(res)
        #pprint.pprint(ast_python.calls)
        #pprint.pprint(ast_python.assigns)

        #for k, v in res.items():
            #if 'Str_s' in k:
                #print(k, v)

def get_var_value(lineno, varname):
    return 'varvalue'


def get_binop_contants(node, args):
    lhs = node.left
    rhs = node.right
    if isinstance(node.op, ast.Add):
        if isinstance(rhs, ast.Constant):
            args.insert(0, rhs.value)
        elif isinstance(rhs, ast.Name):
            value = get_var_value(node.lineno, rhs.id)
            args.insert(0, value)
        else:
            args = None
            return args
        if isinstance(lhs, ast.Constant):
            args.insert(0, lhs.value)
        elif isinstance(lhs, ast.Name):
            value = get_var_value(node.lineno, rhs.id)
            args.insert(0, value)
        elif isinstance(lhs, ast.BinOp):
            get_binop_contants(lhs, args)
        else:
            args = None
            return args
    return args



mod = '''from bisect import bisect_left as bs
import datetime
import time
import numpy as np
from pandas.arrays import *
def foo():
    from re import findall
class Foo():
    def test(self):
        from re import compile as cp, finditer as ft'''
#mod = importlib.import_module(mod)
test_json_ast()