import ast

from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

from models import *
mod = '''from bisect import bisect_left as bs
import datetime as dt
import time
import numpy as np
import testing.alors
from pandas.arrays import hello as b
def foo():
    from re import findall
class Foo():
    def test(self):
        from re import compile as cp, finditer as ft'''

for repo in session.query(Repo).filter(Repo.id == 4):
    print('Getting list of code files  for repo', repo.id)
    cfs = repo.get_code_files()
    print('Getting list of non code files  for repo', repo.id)
    ncfs = repo.get_non_code_files()
    for cf in cfs:
        if cf.code.content:
            ast_code = code_ast(cf.code.content)
            cf.code.visit(root)
            print('Strings found in file ', cf.name)
            for str in cf.code.strs:
                print('     ', str.content)

'''
for comm in session.query(Commit).all():
    print('duplicating commit  number', comm.id)

    commit = models.Commit(id=comm.id, repo_id=comm.repo_id, sha=comm.sha, commit_date=comm.commit_date,
                           author_name=comm.author_name, author_email=comm.author_email,
                           total_modifs=comm.total_modifs)
    models.session.add(commit)
    models.session.commit()

for elem in session.query(Element).yield_per(1):
    print('duplicating Element number', elem.id)
    el = models.Element(id=elem.id, name=elem.name, is_code_file=elem.is_code_file,
                                   repo_id=elem.repo_id, is_folder=elem.is_folder, extension=elem.extension)
    code = models.Code(content=elem.code, json_ast=elem.ast, file_id=elem.id)
    models.session.add(el)
    models.session.add(code)
    models.session.commit()



for commod in session.query(Commit_mod).yield_per(1):
    print('duplicating commit modification number', commod.id)
    com_mod = models.CommitModification(id=commod.id, change_type=commod.change_type,
                                        commit_id=commod.commit_id, file_id=commod.file_id)
    models.session.add(com_mod)
    models.session.commit()



"""
code = models.Code(content=mod)
p = ast.parse(code.content)
code.visit(p)
session.add(code)
session.commit()
for imp in code.imports:
    print(imp.module, imp.alias)"""'''
