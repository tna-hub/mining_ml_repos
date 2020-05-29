from objects import *
import unittest

Base.prepare(engine, reflect=True)
repository = Repo.by_id(16)

class TestRepository(unittest.TestCase):
    def test_repo(self):
        print("{}. Downloading repository {}".format(repository.id, repository.name))
        repository.download()
        print('extract')
        repository.extract_elements()
        print('commits')
        repository.set_commits()
        session.close()

if __name__ == '__main__':
    unittest.main()


