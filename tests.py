from objects import *
import unittest

Base.prepare(engine, reflect=True)
repository = Repo.by_id(120)

class TestRepository(unittest.TestCase):
    def test_repo(self):
        print("{}. Downloading repository {}".format(repository.id, repository.name))
        if repository.download():
            print('extract')
            repository.extract_elements()
            print('commits')
            repository.set_commits()
            session.close()
        else:
            print('    !!! Repository not found or is private. Skipping... !!!')

if __name__ == '__main__':
    unittest.main()


