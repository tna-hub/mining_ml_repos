from objects import *
import shutil
import os
import stat

Base.prepare(engine, reflect=True)


# fixes read only file deletion on windows
def remove_readonly(func, path, _):
    # Clear the readonly bit and reattempt the removal
    os.chmod(path, stat.S_IWRITE)
    func(path)


for repo in session.query(Repo).all():
    print("{}. Downloading repository {}".format(repo.id, repo.name))
    repo.download()
    print("     -Extracting folders and files")
    repo.extract_elements()
    print("     -Extracting commits..., may take a while")
    repo.set_commits()
    print("     -All done! Deleting local repository ".format(repo.name))
    shutil.rmtree(repo.folder_name, onerror=remove_readonly)
