from MerkleTree import MerkleTree
import os

TEST_DIR = "test2"
TEST_FILE = "test2/b/f5.txt"
TEST_FILE_2 = "test2/b/f9.txt"

def get_paths(start_path):
    paths = []

    if os.path.isfile(start_path):
        return [start_path]
    elif os.path.isdir(start_path):
        for child in os.listdir(start_path):
            paths += get_paths(os.path.join(start_path,child))
        return paths
    else:
        raise Exception("Passed path is not a file or directory.")

    return paths

def main():
    paths = get_paths(TEST_DIR)
    tree = MerkleTree(paths)


    path = tree.get_branch(TEST_FILE)
    print tree.audit(TEST_FILE,path)
    print tree.audit(TEST_FILE_2, path)

if __name__ == "__main__":
    main()
