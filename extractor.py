from objects import *
import shutil

Base.prepare(engine, reflect=True)

for repo in session.query(Repo).all():
    print("Downloading repository ", repo.name)
    repo.download()
    print("+++++Extracting folders and files")
    repo.extract_elements()
    print("+++++Extracting commits")
    repo.set_commits()
    print("+++++All done! Deleting local repository", repo.name)
    shutil.rmtree(repo.folder_name)