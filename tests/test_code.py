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


def test_visit_assign_binop():
    ast_test = ast.parse("a = 'test_str_value2' + test_var_name + 'test_str_value0'")
    code = Code()
    code.visit(ast_test)
    ass = code.assigns[0]
    assert ass.code_id == code.id
    assert ass.var_name == 'a'
    assert ass.value is None
    assert ass.refers_to is None
    assert ass.binop is not None
    bin = ass.binop
    assert bin.lineno == 1
    assert bin.assign_id == ass.id
    assert bin.arg_id == None
    assert bin.value is None
    for const in bin.constants:
        assert const.binop_id == bin.id
        if const.cls == 'Str':
            assert const.value == 'test_str_value0' or const.value == 'test_str_value2'
            assert const.position == 0 or const.position == 2
            assert const.var_name is None
        else:
            assert const.cls == 'Var'
            assert const.var_name == 'test_var_name'
            assert const.position == 1
            assert const.value is None

def test_visit_assign_str():
    ast_test = ast.parse("a = 'test_str_value2'")
    code = Code()
    code.visit(ast_test)
    ass = code.assigns[0]
    assert ass.var_name == 'a'
    assert ass.value == 'test_str_value2'
    assert ass.refers_to is None
    assert ass.binop is None


def test_visit_assign_var():
    ast_test = ast.parse("b = test_var_name")
    code = Code()
    code.visit(ast_test)
    ass = code.assigns[0]
    assert ass.var_name == 'b'
    assert ass.value is None
    assert ass.refers_to == 'test_var_name'
    assert ass.binop is None

