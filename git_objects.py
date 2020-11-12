from git import Commit


def

def get_commits(ds=None, code=None, model=None):
    if ds is None and code is None and model is None:
        return Commit.iter_items()