from MerkleTree import MerkleTree
import os

TEST_DIR = "test2"
TEST_FILE_VALID = "test2/b/f5.txt"
TEST_FILE_MISSING = "test2/some/fake/path/f9.txt"

# TODO unit tests
# TODO JSON tests
# TODO change file name
# TODO illustrate how files are tested here. Maybe pretty print?
# TODO typing everywhere
def get_paths(start_path):
    """ Returns a list of relative paths for buildling a merkle tree out of a
        file or directory.
    """
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

# An example of how this might be used:
# Suppose I have a movie on my laptop, and I want
# to give it to you. Then I might build a Merkle Tree out of pieces of the 
# pieces of the movie as files. As I present those files to you, the downloader, I'll 
# present a branch that you can validate using a root hash. This way you
# know I'm not giving you malware or junk.
def main():
    paths = get_paths(TEST_DIR)

    # Seeder builds a merkle tree from the files
    tree = MerkleTree(paths)

    # Seeder gets a branch to prove the file is legitimate
    path = tree.get_branch(TEST_FILE_VALID)

    print(path)
    # Receiver audits the branch is legimitate. They would also need to verify 
    # the root hash of the branch was correct
    print(tree.audit(TEST_FILE_VALID,path))
    print(tree.audit(TEST_FILE_MISSING, path))
    # Presenting all the necessary files and their associated authentication
    # paths is considered a merkle tree traversal. 

if __name__ == "__main__":
    main()
