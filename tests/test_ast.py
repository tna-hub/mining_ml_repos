import ast
from datetime import datetime
import os
import sys
import time

import pytest

from models.asts import Import, ImportFrom
from models.query import windowed_query
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
            code = el.code
            for imp in code.imports:
                print(imp.module)
            for imp in code.import_froms:
                print(imp.module)

            ''' Now set a class as custom func or not.
            a) First look for the name of the function being called in the __init__ function of the class
            b) Second, check the attr of that function if it is None or Not
                -If None, the function name should be present either in the alias or at the end of an element of mods
                -If not None, the function attr should be present in the alias or at the end of an element of mods
                -If not present before, check the func name in native funcs
            '''
            for cls_def in code.class_defs:
                print(cls_def.name)
                # for call in cls_def.calls:


# test_create()
def extract_imports():
    # q = session.query(Code)
    start_time = time.time()
    i = 0
    for cod in session.query(Code).yield_per(100):
        t = (time.time() - start_time) / 60
        if cod.content is not None:
            cod.visit(ast.parse(cod.content))
        if i % 100 == 0:
            session.flush()
            print(datetime.time(datetime.now()), 'Elapsed time: ', t, 'min, code for file:', cod.id, 'Done: ', i,
                  'remaining: ', 2930690 - i)
        i += 1
    print(datetime.time(datetime.now()), 'Committing...')
    session.commit()
        # print(datetime.time(datetime.now()), 'End committing..., Elapsed time:', time.time() - commit_time)


#extract_imports()

