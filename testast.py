import ast

import get_ast
import pprint
#from pattern import ShowStrings


def test(a='hello'):
    hell = 'test'.split(',')[0]
    filename = 'testast.py'
    with open(file=filename, mode='r') as f:
        filename = None
        ast_python = get_ast.code_ast(f.read())
        #print(ast_python.json_ast)
        res = get_ast.flatten_json(ast_python.json_ast)
        pprint.pprint(res)
        pprint.pprint(ast_python.calls)

        #for k, v in res.items():
            #if 'Str_s' in k:
                #print(k, v)


test()
