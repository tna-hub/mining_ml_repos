from objects import *
import unittest

Base.prepare(engine, reflect=True)
repository = Repo.by_id(69)

class TestRepository(unittest.TestCase):
    def test_repo(self):
        print('download')
        repository.download()
        print('extract')
        repository.extract_elements()
        print('commits')
        repository.set_commits()
        session.close()

if __name__ == '__main__':
    unittest.main()


