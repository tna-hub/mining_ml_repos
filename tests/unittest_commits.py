from git import Commit


def test_get_commit_modifying_dataset():
    # TODO
    ds = ""
    for commit in ds.get_commits():
        assert isinstance(commit, Commit)
