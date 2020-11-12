import time

from data_identifier.data_load import CodeFile
from astroid import parse
from git import Repo
import os

from git_objects import init_repo


def main():
    repo = init_repo()
    print(repo.common_dir)
    for commit in repo.get_commits('main.py'):
        print("Committed by %s on %s with sha %s" % (
            commit.committer.name, time.strftime("%a, %d %b %Y %H:%M", time.localtime(commit.committed_date)),
            commit.hexsha))


if __name__ == "__main__":
    main()
