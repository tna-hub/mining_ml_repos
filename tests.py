from objects import *
import unittest

Base.prepare(engine, reflect=True)
#repository = Repo.by_id(1)

class TestRepository(unittest.TestCase):
    def test_repo(self):
        repository.download()
        repository.extract_elements()
        repository.set_commits()

if __name__ == '__main__':
    unittest.main()


