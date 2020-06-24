import ast
import dis
import json
from collections import defaultdict
from pprint import pprint


def classname(cls):
    return cls.__class__.__name__


class code_ast:
    def __init__(self, code):
        self.calls = {}
        self.assigns = []
        self.json_ast = self.make_ast(code)

    def get_assigns(self, node):
        if classname(node) == 'Assign':
            assign = {}
            if hasattr(node, 'targets') and hasattr(node, 'value'):
                if classname(node.value) == 'Str' and classname(node.targets[0]) == 'Name':
                    assign[node.targets[0].id] = node.value.s
                    self.assigns.append(assign)

    def get_calls(self, node):
        if classname(node) == 'Call':
            infos = {}
            attr_value = None
            arguments = []

            if hasattr(node.func, 'attr'):
                name = node.func.attr
                if classname(node.func.value) == 'Name':
                    attr_value = node.func.value.id
            elif hasattr(node.func, 'id'):
                name = node.func.id
            if hasattr(node, 'args'):
                i = 0
                for arg in node.args:
                    if classname(arg) == 'Str':
                        argument = {}
                        argument['type'] = 'str'
                        argument['position'] = i
                        argument['value'] = arg.s
                        arguments.append(argument)
                    elif classname(arg) == 'Name':
                        argument = {}
                        argument['type'] = 'var'
                        argument['position'] = i
                        argument['varname'] = arg.id
                        argument['value'] = None
                        found = False
                        for var in reversed(self.assigns):
                            for key in var.keys():
                                if key == arg.id:
                                    argument['value'] = var[key]
                                    found = True
                            if found:
                                break
                        arguments.append(argument)

                    i = i + 1
                infos['attr_value'] = attr_value
                infos['args'] = arguments
            if hasattr(node, 'keywords'):
                for keyword in node.keywords:
                    if hasattr(keyword, 'arg') and hasattr(keyword, 'value'):
                        if classname(keyword.value) == 'Str':
                            argument = {}
                            argument['type'] = 'str'
                            argument['position'] = keyword.arg
                            argument['value'] = keyword.value.s
                            arguments.append(argument)
                        elif classname(keyword.value) == 'Name':
                            argument = {}
                            argument['type'] = 'var'
                            argument['position'] = keyword.arg
                            argument['varname'] = keyword.value.id
                            argument['value'] = None
                            found = False
                            for var in reversed(self.assigns):
                                for key in var.keys():
                                    if key == keyword.value.id:
                                        argument['value'] = var[key]
                                        found = True
                                if found:
                                    break
                            arguments.append(argument)

                infos['attr_value'] = attr_value
                infos['args'] = arguments
            self.calls[name] = infos

    def jsonify_ast(self, node, level=0):
        fields = {}
        if hasattr(node, '_fields'):
            self.get_assigns(node)
            self.get_calls(node)
            for k in node._fields:
                fields[k] = '...'
                v = getattr(node, k)
                if isinstance(v, ast.AST):
                    if v._fields:
                        fields[k] = self.jsonify_ast(v)
                    else:
                        fields[k] = classname(v)

                elif isinstance(v, list):
                    fields[k] = []
                    for e in v:
                        fields[k].append(self.jsonify_ast(e))

                elif isinstance(v, str):
                    if v == float('inf'):
                        fields[k] = str(v)
                    else:
                        fields[k] = v

                elif isinstance(v, int) or isinstance(v, float):
                    if v == float('inf'):
                        fields[k] = str(v)
                    else:
                        fields[k] = v

                elif v is None:
                    fields[k] = None

                else:
                    fields[k] = 'unrecognized'

        ret = {classname(node): fields}
        return ret

    def make_ast(self, code):
        try:
            tree = ast.parse(code)
            return self.jsonify_ast(tree)
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
