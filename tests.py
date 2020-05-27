from objects import *
import unittest

Base.prepare(engine, reflect=True)
repository = Repo.by_id(1)
class TestRepository(unittest.TestCase):
    def test_repo_name(self):
        self.assertEqual(repository.folder_name, "tf_mesh_renderer", "Should be tf_mesh_renderer")

    def test_download(self):
        self.assertEqual(repository.download(), True, "Should be True")

    def test_downloaded(self):
        self.assertEqual(os.path.isdir(repository.folder_name), True, "Should be True")
    def test_extract(self):
        repository.extract_elements()
if __name__ == '__main__':
    unittest.main()


