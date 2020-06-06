from objects import *


Base.prepare(engine, reflect=True)

modules = []

def do_add(s, x):
    length = len(s)
    s.add(x)
    return len(s) != length


def set_mods():
    for i in range(2,14166):
        repo_mods = set()
        for file in session.query(Element).filter(Element.repo_id == i,
                                                  Element.is_code_file == True):
            imports = file.imports
            if imports is not None:
                for mod in imports.split(','):
                    if mod != '':
                        do_add(repo_mods, mod)
        if len(repo_mods) > 0:
            print(len(repo_mods), 'unique modules of repository', i)
            modules.append(list(repo_mods))

set_mods()
