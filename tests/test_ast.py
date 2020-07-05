import ast

import pytest
from models.asts import Assign, BinOp, Constant, Argument
import sys, os

from models.config import session_scope

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

code_test = '''
a = 'first var'
b = a
def foo():
    c = a + b
'''

with session_scope() as s:
    session = s


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


@pytest.mark.parametrize("id, binop_id, var_name, cls, value, position", [
    (1, 1, None, 'Str', 'test_var_value1', 1),
    (2, 1, 'test_var_name2', 'Var', None, 2)
])
def test_constant(id, binop_id, var_name, cls, value, position):
    const = Constant(id=id, binop_id=binop_id, var_name=var_name,
                     cls=cls, value=value, position=position)

    assert const.id == id
    assert const.binop_id == binop_id
    assert const.var_name == var_name
    assert const.cls == cls
    assert const.value == value
    assert const.position == position


def test_binop():
    binop = BinOp(id=1,
                  lineno=1,
                  value='test_var_value',
                  arg_id=1,
                  assign_id=None)
    assert binop.id == 1
    assert binop.lineno == 1
    assert binop.value == 'test_var_value'
    assert binop.assign_id is None


@pytest.mark.skip(reason="Already tested, will create duplicates in the database")
def test_binop_constants():
    binop = BinOp(lineno=1,
                  value=None,
                  arg_id=None,
                  assign_id=None)

    binop.constants.append(Constant(id=1, var_name='test_var_name',
                                    cls='Str', value='test_var_value', position=0))
    binop.constants.append(Constant(id=2, var_name='test_var_name',
                                    cls='Var', value=None, position=1))
    session.add(binop)
    session.commit()
    for const in binop.constants:
        assert const.id == 1 or const.id == 2
        assert const.binop_id == binop.id
        assert const.var_name == 'test_var_name' or const.var_name is None
        assert const.cls == 'Var' or const.cls == 'Str'
        assert const.value is None or const.value == 'test_var_value'
        assert const.position == 0 or const.position == 1



def test_set_binop_constants():
    code = ast.parse("'test_str_value2' + test_var_name + 'test_str_value0'")
    binop = BinOp(lineno=code.body[0].value.lineno,
                  value=None,
                  arg_id=None,
                  assign_id=None)
    binop.set_constants(code.body[0].value)
    session.add(binop)
    session.commit()
    for const in binop.constants:
        assert const.binop_id == binop.id
        if const.cls == 'Str':
            assert const.value == 'test_str_value0' or const.value == 'test_str_value2'
            assert const.position == 0 or const.position == 2
            assert const.var_name is None
        else:
            assert const.cls == 'Var'
            assert const.var_name == 'test_var_name'
            assert const.position == 1
            assert const.value is None

    code = ast.parse("'test_str_value2' + test_var_name + 'test_str_value0'")