from MerkleTree import MerkleTree
from typing import * 
import os
import unittest

TEST_DIR = "test2"
TEST_FILE_VALID = "test2/b/f5.txt"
TEST_FILE_MISSING = "test2/some/fake/path/f9.txt"

# An example of how this might be used:
# Suppose I have a movie on my laptop, and I want
# to give it to you. Then I might build a Merkle Tree out of pieces of the 
# pieces of the movie as files. As I present those files to you, the downloader, I'll 
# present an authentication path that you can validate using a root hash you
# trust. Because it would be computionally infeasible to do build a fake
# authentication path, you can trust the data, even though you don't know the sender. 
class TestMerkleTreeFiles(unittest.TestCase):

    def setUp(self):
        self.paths = self._get_paths(TEST_DIR)
        # Seeder builds a merkle tree from the files
        self.tree = MerkleTree(self.paths)

    def test_get_branch(self):
        # Seeder gets a branch to prove the file is legitimate
        path = self.tree.get_branch(TEST_FILE_VALID)

        # Manually hash files for expected case
        expected = ['5218c7782483dfd025fbefbfe726d62c', 'f17774a88c7b26e7c334f572b2964be2', '8b888d3e673e3134fd2d696da568ed11']
        self.assertEqual(expected, path)

    def test_audit(self):
        path = self.tree.get_branch(TEST_FILE_VALID)

        self.assertTrue(self.tree.audit(TEST_FILE_VALID,path))
        self.assertFalse(self.tree.audit(TEST_FILE_MISSING, path))
    
    def test_traverse(self):
        result = self.tree.traverse()
        self.assertEqual(len(result), 6)
        self.assertEqual(len(result[0][1]), 3)
        self.assertEqual(len(result[4][1]), 4)
        
    def _get_paths(self, start_path) -> List[str]:
        """ Returns a list of relative paths for buildling a merkle tree out of a
            file or directory.

            Directory structure of test2:
            
            test2
            ├── a
            │   ├── d
            │   │   └── f1.txt
            │   ├── f2.txt
            │   └── f3.txt
            ├── b
            │   └── f5.txt
            ├── c
            │   └── something.txt
            └── hi.txt
        """
        paths = []
    
        if os.path.isfile(start_path):
            return [start_path]
        elif os.path.isdir(start_path):
            for child in os.listdir(start_path):
                paths += self._get_paths(os.path.join(start_path,child))
            return paths
        else:
            raise Exception("Passed path is not a file or directory.")
    
        return paths

if __name__ == "__main__":
    unittest.main()
