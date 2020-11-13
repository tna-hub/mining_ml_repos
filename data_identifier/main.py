import json

from data_identifier.data_load import CodeFile
from astroid import parse
from pathlib import Path


def load_function_names(path: str = 'functions.json') -> object:
    """
    :param path:
    :return: The list of functions names to search for
    """
    names = {}
    try:
        with open(path) as f:
            data = json.load(f)
            for key, value in data.items():
                for k, v in value.items():
                    if k not in names.keys():
                        names[k] = v['set_mode_from_name']
    except Exception as e:
        raise e
    return names


def extract(directory: str):
    p = Path(directory)
    names = load_function_names()
    for file in p.glob('**/*.py'):
        with open(file) as f:
            module = parse(f.read())
            cf = CodeFile(astroid_node=module, name=file.name, filename=file.absolute().relative_to(Path.cwd()),
                          project_name=directory)
            for opn in cf.get_open_node(names):
                print(opn.full_name, end=': ')
                for arg in opn.args:
                    print(arg.value, end='')
                    if arg.position == 0:
                        print(':'+str(opn.io), end='; ')
                print()


def main():
    pass


if __name__ == "__main__":
    extract('../tests/git_repos_test1')
