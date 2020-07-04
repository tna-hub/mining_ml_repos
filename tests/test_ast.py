import pytest
from models.asts import Assign
import sys, os


myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

code = '''
a = 'first var'
b = a
def foo():
    c = a + b
'''


@pytest.mark.parametrize("id, lineno, code_id, var_name, refers_to, value", [
    (1, 7, 1, 'test_var_name', 'test_var_refers_to', 'test_var_value'),
    (2, 8, 3, 'test_var_name', None, None)
])
def test_assign(id, lineno, code_id, var_name, refers_to, value):
    ass = Assign(id=id, lineno=lineno, code_id=code_id, var_name=var_name, refers_to=refers_to, value=value)
    assert ass.id == id
    assert ass.lineno == lineno
    assert ass.code_id == code_id
    assert ass.var_name == var_name
    assert ass.refers_to == refers_to
    assert ass.value == value
