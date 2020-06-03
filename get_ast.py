import ast
import dis
import json
from collections import defaultdict
from pprint import pprint


def classname(cls):
    return cls.__class__.__name__

def jsonify_ast(node, level=0):
    fields = {}
    if hasattr(node, '_fields'):
        for k in node._fields:
            fields[k] = '...'
            v = getattr(node, k)
            if isinstance(v, ast.AST):
                if v._fields:
                    fields[k] = jsonify_ast(v)
                else:
                    fields[k] = classname(v)

            elif isinstance(v, list):
                fields[k] = []
                for e in v:
                    fields[k].append(jsonify_ast(e))

            elif isinstance(v, str):
                fields[k] = v

            elif isinstance(v, int) or isinstance(v, float):
                fields[k] = v

            elif v is None:
                fields[k] = None

            else:
                fields[k] = 'unrecognized'

    ret = { classname(node): fields }
    return ret


def make_ast(code):
    try:
        tree = ast.parse(code)
        return jsonify_ast(tree)
    except Exception as e:
        return {'error': "{}".format(e)}


def flatten_json(nested_json):
    """
        Flatten json object with nested keys into a single level.
        Args:
            nested_json: A nested json object.
        Returns:
            The flattened json object if successful, None otherwise.
    """
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(nested_json)
    return out

def get_key(dict, val):
    keyval = {}
    for key, value in dict.items():
        if isinstance(value, str):
            if val in value:
                keyval[key] = value
    return keyval


def get_modules(code):
    instructions = dis.get_instructions(code)
    imports = [__ for __ in instructions if 'IMPORT' in __.opname]

    grouped = defaultdict(list)
    for instr in imports:
        grouped[instr.opname].append(instr.argval)

    libraries = set()
    for lib in grouped['IMPORT_NAME']:
        libr = lib.split('.')[0]
        libraries.add(libr)

    return ','.join(list(libraries))