import ast
from get_ast import jsonify_ast

from astcheck import assert_ast_like, listmiddle, name_or_attr
from astsearch import (
    prepare_pattern, ASTPatternFinder, must_exist_checker, must_not_exist_checker,
    ArgsDefChecker,
)


def get_matches(pattern, sample_code):
    sample_ast = ast.parse(sample_code)
    print(ast.dump(sample_ast))
    return list(ASTPatternFinder(pattern).scan_ast(sample_ast))


code = """
import name
'ulyfutgou'.split('noway')
def function(name):
    print('func255')
a = 'blah'
b = '''multi
line
string'''
c = u"spam"
test()
with open('laststring') as f:
    pass
"""

root = ast.parse(code)


class ShowStrings(ast.NodeVisitor):
    def visit_Str(self, node):
        print("string", repr(node.s))
        print(node)

    def visit_Call(self, node):
        #print(jsonify_ast(node))
        #print(node.__dict__)
        if hasattr(node.func, 'attr'):
            print("function call", repr(node.func.attr))
        elif hasattr(node.func, 'id'):
            print("function call", repr(node.func.id))
        #print(node)



show_strings = ShowStrings()
show_strings.visit(root)
