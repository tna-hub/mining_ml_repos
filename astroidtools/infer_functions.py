from astroid import Const
from astroid.exceptions import InferenceError
from astroid import MANAGER, nodes, inference_tip
import os


def _looks_like_infer_join(node, node_name="join"):
    print("hellooo")
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
    # TODO: Set working dir for os no to get confused between thisfile dir and the target directory
    new_node = call_node
    success = True
    ags = []
    for arg in call_node.args:
        try:
            val = next(arg.infer())
            if val.__class__.__name__ != "Const":
                success = False
                new_node = val
            else:
                ags.append(val.value)
        except InferenceError as e:
            new_node = e
            success = False

    if success:
        new_node = Const(value=os.path.join(*ags))
    return iter((new_node,))


def register_transformations():
    MANAGER.register_transform(
        nodes.Call,
        inference_tip(infer_join),
        _looks_like_infer_join,
    )


f = os.path.dirname(__file__)
print("hellooo", __file__)
