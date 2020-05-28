from objects import *
import shutil

import logging

logging.basicConfig(filename='app.log',
                    filemode='w',
                    format='%(message)s',
                    level=logging.DEBUG)

Base.prepare(engine, reflect=True)

for repo in session.query(Repo).all():
    logging.info("{}. Downloading repository {}".format(repo.id,  repo.name))
    repo.download()
    logging.info("-----Extracting folders and files")
    repo.extract_elements()
    logging.info("-----Extracting commits")
    repo.set_commits()
    logging.info("-----All done! Deleting local repository ".format(repo.name))
    shutil.rmtree(repo.folder_name)

