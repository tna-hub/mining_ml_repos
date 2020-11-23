import json
import os
import csv

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


def extract_to_csv(directory, file: str = '.extracted.csv'):
    """
    Writes the results of the data identification a csv file

    :param str directory:
    :param file:
    :return:
    """
    with open(file, 'w') as f:
        fnames = ['a_name', 'loaded_in', 'io', 'lineno']
        writer = csv.DictWriter(f, fieldnames=fnames)
        writer.writeheader()
        for opn in extract(directory):
            for arg in opn.args:
                if arg.position == 0 and arg.value_found:
                    to_write = {
                        'a_name': arg.value,
                        'loaded_in': str(opn.filename),
                        'io': opn.io,
                        'lineno': arg.lineno
                    }
                    writer.writerow(to_write)


def extract(directory: str):
    p = Path(directory)
    names = load_function_names()
    for file in p.glob('**/*.py'):
        with open(file) as f:
            module = parse(f.read())
            cf = CodeFile(astroid_node=module, name=file.name,
                          filename=file.relative_to(directory),
                          project_name=directory)
            for opn in cf.get_open_node(names):
                yield opn


def main():
    pass


if __name__ == "__main__":
    folder = "../tests/saner/"
    listing = [n for n in os.listdir(os.path.abspath(folder)) if os.path.isdir(folder+n)]
    for li in listing:
        print("Extracting for", li)
        try:
            extract_to_csv(folder+li, li+'.csv')
        except Exception:
            print("      Error")
