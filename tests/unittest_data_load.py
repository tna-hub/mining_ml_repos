import pytest
from pytest import raises

from astroidtools import infer_functions as ifs
from astroid import parse

from data_identifier.data_load import CodeFile, ASTObject, DataLoadFunc, Arg


@pytest.fixture
def file_from_source():
    """Returns a CodeFile Object instance with source as content"""
    source = '''
    f = "filename.2"
    c = os.path.join("root", "dir1")
    d = os.path.join(c, "dir2")
    open1(c+"/filename.1", "r", sep=";")
    with open2(file=os.path.join(d, f), mode="w+"):
        pass
    '''
    module = parse(source)
    return CodeFile(astroid_node=module, name="filename1.py", filename="root/project1/filename1.py",
                    project_name="project1")


@pytest.mark.parametrize("object", [
    "ASTObject",
    "CodeFile",
    "DataLoadFunc",
    "Arg"
])
def test_empty_astroid_node_object(object):
    with raises(ValueError) as e:
        eval(object + "()")
    assert e.type is ValueError
    assert e.value.args[0] == f'The astroid node for Object {object} should not be empty'


def test_file_params(file_from_source):
    # TODO: Add tests for CodeFile Object parameters
    pass


def test_file_open_funcs(file_from_source):
    funcs = list(file_from_source.get_open_node(names=["open1", "open2"]))
    assert len(funcs) == 2
    for obj in funcs:
        assert isinstance(obj, DataLoadFunc)
        for arg in obj.args:
            assert isinstance(arg, Arg)
    assert funcs[0].name == "open1"
    assert len(funcs[0].args) == 3
    assert funcs[1].name == "open2"
    assert len(funcs[1].args) == 2


@pytest.mark.parametrize("function,id,position,name,value,value_found", [
    ("open1", 0, 0, None, "root/dir1/filename.1", True),
    ("open1", 1, 1, None, "r", True),
    ("open1", 2, 2, "sep", ";", True),
    ("open2", 0, 0, "file", "root/dir1/dir2/filename.2", True),
    ("open2", 1, 1, "mode", "w+", True)
])
def test_open_funcs_args(file_from_source, function, id, position, name, value, value_found):
    for obj in file_from_source.get_open_node(names=["open1", "open2"]):
        if obj.name == function:
            assert obj.args[id].position == position
            assert obj.args[id].name == name
            assert obj.args[id].value == value
            assert obj.args[id].value_found == value_found



