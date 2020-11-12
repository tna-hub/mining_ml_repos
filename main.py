
from data_identifier.data_load import File
from astroid import parse
from git import Repo
import os


def init_repo(path=None):
    if path is None:
        return Repo(os.path.dirname(__file__))
    else:
        return Repo(os.path.dirname(path))

def main():
    print(init_repo().common_dir)


if __name__ == "__main__":
    main()
