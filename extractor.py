from objects import *
import shutil

Base.prepare(engine, reflect=True)

for repo in session.query(Repo).all():
    print("{}. Downloading repository {}".format(repo.id,  repo.name))
    repo.download()
    print("     -Extracting folders and files")
    repo.extract_elements()
    print("     -Extracting commits..., may take a while")
    repo.set_commits()
    print("     -All done! Deleting local repository ".format(repo.name))
    shutil.rmtree(repo.folder_name, ignore_errors=False, onerror=None)

