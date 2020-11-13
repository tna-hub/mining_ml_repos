import time

from data_identifier.data_load import CodeFile
from astroid import parse
from git import Repo
import os

from git_objects import init_repo
from pprint import pprint


def main():
    repo = init_repo()
    for commit in repo.get_commits('main.py', 'extractor.py'):
        print("Committed by %s on %s with sha %s" % (
            commit.committer.name, time.strftime("%a, %d %b %Y %H:%M", time.localtime(commit.committed_date)),
            commit.hexsha))
        pprint(commit.stats.files)


if __name__ == "__main__":
    main()
