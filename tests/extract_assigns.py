import ast
from datetime import datetime
import os
import sys
import time

from models.code import Code
from models.config import session_scope
from models import gits, code, func_load_files, asts
from models.func_load_files import NativeFunc, LibFunc

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


def get_load_funcs():
    with session_scope() as session:
        native_funcs = session.query(NativeFunc).all()
        lib_funcs = session.query(LibFunc).all()


nat_lib_names = ['numpy', 'pandas']

with session_scope() as s:
    session = s


def test_create():
    test_repo = '../data/test_repo/model.py'
    repo = gits.Repo(folder_name='../data/test_repo')
    repo.extract_elements()
    for el in repo.elements:
        if el.is_code_file:
            el.code.visit(ast.parse(el.code.content))
            cod = el.code
            print(el.name)
            for assign in cod.assigns:
                print(assign.target, assign.ast_object.cls, assign.ast_object.value)

            ''' Now set a class as custom func or not.
            a) First look for the name of the function being called in the __init__ function of the class
            b) Second, check the attr of that function if it is None or Not
                -If None, the function name should be present either in the alias or at the end of an element of mods
                -If not None, the function attr should be present in the alias or at the end of an element of mods
                -If not present before, check the func name in native funcs
            
            #for cls_def in code.class_defs:
                #print(cls_def.name)
                # for call in cls_def.calls:
                    #pass'''


# test_create()


def extract_assigns():
    # q = session.query(Code)
    start_time = time.time()
    i = 0
    for cod in session.query(Code).yield_per(100):
        t = (time.time() - start_time) / 60
        if cod.content is not None:
            try:
                cod.visit(ast.parse(cod.content))
            except Exception:
                pass
            #for ass in cod.assigns:
                #print(str(cod.id) + ':', ass.target, ass.lineno, ass.ast_object.cls, ass.ast_object.var_name, ass.ast_object.value)
        if i % 1000 == 0:
            try:
                session.flush()
                print(datetime.time(datetime.now()), 'Elapsed time: ', t, 'min, code info for file:', cod.id, 'Done: ', i, 'remaining: ', 2930690-i)
            except Exception:
                pass
        i += 1
    commit_time = datetime.time(datetime.now())
    print(commit_time, 'Committing...')
    session.commit()
    print(datetime.time(datetime.now()), 'End committing..., Elapsed time:', time.time() - commit_time)

extract_assigns()
