from astroidtools import infer_functions as ifs
from astroid import parse


def test_infer_join():
    source = "os.path.join('dir', 'file.name')"
    node = parse(source).body[0].value
    value = next(node.infer())
    assert value.__class__.__name__ == "Const"
    assert value.value == "dir/file.name"
