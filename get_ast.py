import ast
import json

def classname(cls):
    return cls.__class__.__name__

def jsonify_ast(node, level=0):
    fields = {}
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
    tree = ast.parse(code)
    return jsonify_ast(tree)


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

#def get_data()

def test():
    file = open("get_ast.py", "r")
    filey = "get_ast_filey.csv"
    f = file.read()
    file.close()
    jso = make_ast(f)
    flat = flatten_json(jso)
    print(json.dumps(flat, indent=True))
    print(get_key(flat, "get_ast"))
