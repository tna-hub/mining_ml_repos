from objects import *
import shutil
import os
import stat

Base.prepare(engine, reflect=True)


# fixes read only file deletion on windows
def remove_readonly(func, path, _):
    # Clear the readonly bit and reattempt the removal
    print("One error")
    os.chmod(path, stat.S_IWRITE)
    func(path)


for repo in session.query(Repo).filter(Repo.id > 999, Repo.id < 2000).all():
    print("{}. Downloading repository {}".format(repo.id, repo.name))
    try:
        if repo.download():
            print("     -Extracting folders and files")
            repo.extract_elements()
            print("     -Extracting commits")
            repo.set_commits()
            print("     -All done! Deleting local repository ".format(repo.name))
            shutil.rmtree(repo.folder_name, onerror=remove_readonly)
        else:
            print('    !!! Repository not found or is private. Skipping... !!!')
    except Exception as e:
        print("Error:", e)

print('=================Finished Extraction! Everything was inserted to the database!===========================')
