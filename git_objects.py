import git
import os


class Repo(git.Repo):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_commits(self, ds=None, code=None, model=None):
        paths = []
        if ds is not None:
            paths.append(ds)
        if code is not None:
            paths.append(code)
        if model is not None:
            paths.append(model)
        if len(paths) == 0:
            raise ValueError('Must provide at least one parameter to get the commits for')
        else:
            return self.iter_commits('--all', paths=paths)


def init_repo(path=None):
    if path is None:
        return Repo(os.getcwd())
    else:
        return Repo(path)
