from astroid import parse, Const
from astroid.exceptions import InferenceError
from astroid import MANAGER, nodes, inference_tip
import os
import json


def _looks_like_infer_join(node, node_name="join"):
    if node.__class__.__name__ == "Call":
        name = ""
        if hasattr(node.func, "id"):
            name = node.func.id
        elif hasattr(node.func, "attrname"):
            name = node.func.attrname
        if name == node_name:
            return True
    return False


def infer_join(call_node, context=None):
    new_node = call_node
    # Do some transformation here
    # set the working dir
    success = True
    ags = []
    for arg in call_node.args:
        try:
            val = next(arg.infer())
            if val.__class__.__name__ != "Const":
                success = False
                new_node = InferenceError("Could not infer the value for " + str(call_node.as_string()))
            else:
                ags.append(val.value)
        except InferenceError as e:
            print(e)
            success = False
            break

    if success:
        new_node = Const(value=os.path.join(*ags))
    return iter((new_node,))


MANAGER.register_transform(
    nodes.Call,
    inference_tip(infer_join),
    _looks_like_infer_join,
)


def get_open_node(start_from, names):
    res = []
    nn = None
    for n in start_from.nodes_of_class(nodes.Call):
        if hasattr(n.func, "attrname"):
            nn = n.func.attrname
        elif hasattr(n.func, "name"):
            nn = n.func.name
        if nn is not None and nn in names:
            res.append(n)
    return res


# def format_open_func_args(node)

source = '''
import os
from test import Test

f = "hello.png"
t = Test(filename="testingoh")
c = os.path.join("root", t.filename)
d = os.path.join(c, "dir2")
open(c, gigi="hi", mode="testing")
t.opening(os.path.join(d, "hello.jo"), oro="r", **kwargs)
'''
module = parse(source)


# print(get_open_node(module, "opening")[0].as_string())
def get_v(object):
    v = None
    try:
        v = next(object.infer())
    except Exception as e:
        v = e
    if v.__class__.__name__ == "Const":
        return v.value
    else:
        return f"Error::{v.__class__.__name__}::{str(v)}"


def get_keywords(node, index=0):
    keywords = []
    for i, keyword in enumerate(node.keywords):
        index += i
        v = get_v(keyword.value)
        keywords.append({
            "position": index,
            "name": keyword.arg,
            "value": v
        })
    return keywords


def get_args(node, index=0):
    args = []
    for i, arg in enumerate(node.args):
        index = i
        v = get_v(arg)
        args.append({
            "position": index,
            "name": None,
            "value": v
        })
    return args, index + 1


for node in get_open_node(module, ["opening", "open"]):
    # print(node)
    d = {'name': node.func.name if hasattr(node.func, "name") else node.func.attrname, 'lineno': node.lineno,
         'args': []}
    last = 0
    if node.args is not None:
        d['args'], last = get_args(node)
    if node.keywords is not None:
        d['args'] += get_keywords(node, last)
    print(json.dumps(d, indent=4))
    # print(next(node.keywords[0].value.infer()))

# print(module.body[-1].repr_tree())

# print(next(module.body[-1].value.args[1].infer()))
# print(module.as_string())
