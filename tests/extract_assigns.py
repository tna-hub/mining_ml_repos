import ast
import traceback
from datetime import datetime
import os
import sys
import time

from sqlalchemy.orm import load_only

from models.asts import emoji_pattern
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


#test_create()

def extract_assigns():
    # q = session.query(Code)
    start_time = time.time()
    q = session.query(Code).options(load_only("id", "content"))
    i = 0
    for cod in q.yield_per(1000):#q.filter(Code.id > 630498, Code.id < 630501):.yield_per(10000):
        try:
            content = cod.content
        except Exception:
            session.rollback()
            e = sys.exc_info()
            print('Error when fetching', i)
            print(traceback.format_exc())
            exit()

            #continue
        try:
            if cod is not None:
                if content is not None:
                    cod.visit(ast.parse(content))
        except Exception as e:
            e = sys.exc_info()
            print('Error when visiting', i)
            print(traceback.format_exc())
            exit()
            continue
                #for ass in cod.assigns:
                    #print(str(cod.id) + ':', ass.target, ass.lineno, ass.ast_object.cls, ass.ast_object.var_name, ass.ast_object.value)
        if i % 1000 == 0:
            try:
                if cod is not None:
                    #cod.content = emoji_pattern.sub(r'', cod.content)
                    session.flush()
                    t = (time.time() - start_time) / 60
                    print(datetime.time(datetime.now()), 'Elapsed time: ', t, 'min, code info for file:', cod.id, 'Done: ', i, 'remaining: ', 2930690-i)
            except Exception as e:
                session.rollback()
                e = sys.exc_info()
                print('Error when flushing', cod.id)
                print(traceback.format_exc())
                exit()
        i += 1
    commit_time = time.time()
    print(commit_time, 'Committing...')
    session.flush()
    session.commit()
    print(datetime.time(datetime.now()), 'End committing..., Elapsed time:', time.time() - commit_time)

#extract_assigns()
def test_open():
    q = session.query(Code).options(load_only("id", "content"))
    for cod in q.yield_per(1000):
        if cod.content is not None:
            cod.visit(ast.parse(cod.content))

#test_open()
fs = 'open,load,loadtxt,save,savez,savez_compressed,savetxt,memmap,chararray.dump,chararray.tofile,recarray.dump,' \
     'recarray.tofile,open,load,save,io.read_file,io.write_file,keras.models.save_model,keras.models.load_model,' \
     'keras.utils.get_file,load_data,load,datasets.load_files,Image.open,Dataframe.to_csv,read_csv,read_excel,' \
     'read_pickle,read_table,ExcelWriter,read_spss,read_fwf,model.save,imread,open,open_code,io.imread,io.imsave,File'
f = fs.split(',')
funcs = []
final = ''
for ff in f:
    funcs.append(ff.split('.')[-1])
for ff in funcs:
    final += ff +','

print(final)
