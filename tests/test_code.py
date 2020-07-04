import ast

import pytest
from models.asts import Assign
from models.code import Code
from models.config import session_scope
import sys, os

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

code_test = '''
a = 'first var'
b = a
def foo():
    c = a + b
'''
ast_test = ast.parse(code_test)

with session_scope() as s:
    session = s


@pytest.fixture
def code():
    """Returns a code object from the database with id == 7"""
    code = session.query(Code).filter(Code.id == 7).one()
    return code


def test_code(code):
    assert code.id == 7


@pytest.mark.parametrize("lineno, code_id, var_name, refers_to, value", [
    (7, 1, 'test_var_name', 'test_var_refers_to', 'test_var_value'),
    (8, 3, 'test_var_name', None, None)
])
@pytest.mark.skip(reason="Already tested, will create duplicates in the database")
def test_code_assign(code, lineno, code_id, var_name, refers_to, value):
    ass = Assign(lineno=lineno, var_name=var_name, refers_to=refers_to, value=value)
    code.assigns.append(ass)
    session.commit()
    assert ass.code_id == 7


@pytest.mark.parametrize("index, var_name, value, refers_to", [
    (0, 'a', 'first var', None),
    (1, 'b', None, 'a'),
    (2, 'c', None, None)
])
def test_visit_assign(code, index, var_name, value, refers_to):
    code.visit(ast_test)
    assert code.assigns[index].var_name == var_name
    assert code.assigns[index].value == value
    assert code.assigns[index].refers_to == refers_to


