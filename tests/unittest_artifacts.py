import pytest
from pytest import raises
from artifacts import *


@pytest.mark.parametrize("object", [
    "Artifact",
    "Dataset",
    "Model",
    "Config",
    "Code",
    "Params"
])
def test_empty_artifact_path(object):
    with raises(ValueError) as e:
        eval(object + "()")
    assert e.type is ValueError
    assert e.value.args[0] == f'The path for Object {object} should not be empty'