import ast

import get_ast
import pprint
from pattern import ShowStrings


def test(a='hello'):
    hell = 'test'.split(',')[0]
    with open('testast.py') as f:
        pprint.pprint(get_ast.flatten_json(get_ast.make_ast(f.read())))


test()