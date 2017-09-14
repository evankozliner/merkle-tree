import unittest
import hashlib
from MerkleTree import MerkleTree

ONE_ELEMENT_DATA = "text"
TWO_ELEMENT_DATA = ["one", "two"]
THREE_ELEMENT_DATA = ["one", "two", "three"]

def md5sum(data):
    data = str(data)
    m = hashlib.md5()
    m.update(data)
    return m.hexdigest()

class TestMerkleTree(unittest.TestCase):
    def test_empty_tree_error(self):
        with self.assertRaises(Exception) as cm:
            tree = MerkleTree([])

    def test_one_element_tree(self):
        tree = MerkleTree([ONE_ELEMENT_DATA])
        expected_root_hash = md5sum(ONE_ELEMENT_DATA)

        self.assertEqual(expected_root_hash, tree.root_hash)
        self.assertEqual(0, tree.max_height)

    def test_two_element_tree(self):
        tree = MerkleTree(TWO_ELEMENT_DATA)
        expected_root_hash = md5sum(md5sum(TWO_ELEMENT_DATA[0]) + \
                md5sum(TWO_ELEMENT_DATA[1]))
        self.assertEqual(expected_root_hash, tree.root_hash)
        self.assertEqual(1, tree.max_height)

    def test_three_element_tree(self):
        tree = MerkleTree(THREE_ELEMENT_DATA)
        expected_root_hash = md5sum(md5sum(THREE_ELEMENT_DATA[0]) + \
                md5sum(md5sum(THREE_ELEMENT_DATA[1]) + \
                md5sum(THREE_ELEMENT_DATA[2])))
        self.assertEqual(expected_root_hash, tree.root_hash)
        self.assertEqual(2, tree.max_height)
        self.assertEqual(5, len(tree.node_table.keys()))

    def test_one_element_audit(self):
        false_data = "not in tree"
        data_hash = md5sum(ONE_ELEMENT_DATA)
        data_hash_false = md5sum(false_data)
        tree = MerkleTree([ONE_ELEMENT_DATA])
        result_true = tree.audit(ONE_ELEMENT_DATA, [data_hash])
        result_false = tree.audit(false_data, [data_hash_false])

        self.assertTrue(result_true)
        self.assertFalse(result_false)

    def test_two_element_audit_valid(self):
        tree = MerkleTree(TWO_ELEMENT_DATA)
        result = tree.audit(TWO_ELEMENT_DATA[0], [md5sum(TWO_ELEMENT_DATA[1])])
        self.assertTrue(result)

    def test_three_element_hanging_node_audit(self):
        tree = MerkleTree(THREE_ELEMENT_DATA)
        proof = [md5sum(md5sum(THREE_ELEMENT_DATA[1]) + \
                md5sum(THREE_ELEMENT_DATA[2]))]
        result = tree.audit(THREE_ELEMENT_DATA[0], proof)
        self.assertTrue(result)

    def test_three_element_valid(self):
        tree = MerkleTree(THREE_ELEMENT_DATA)
        proof = [ md5sum(THREE_ELEMENT_DATA[0]),md5sum(THREE_ELEMENT_DATA[1]) ]
        result = tree.audit(THREE_ELEMENT_DATA[2], proof)
        self.assertTrue(result)

    def test_three_element_invalid(self):
        return

    def test_three_element_auth_path(self):
        tree = MerkleTree(THREE_ELEMENT_DATA)
        result = tree.get_branch("one")
        sibling_hash = md5sum(md5sum(THREE_ELEMENT_DATA[1]) + \
                md5sum(THREE_ELEMENT_DATA[2]))
        self.assertEqual(result, 
                [md5sum(md5sum(THREE_ELEMENT_DATA[0]) + sibling_hash),
                 sibling_hash])

if __name__ == "__main__":
    unittest.main()

