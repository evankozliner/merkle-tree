""" Evan Kozliner """

import os
import math
import hashlib
import copy

class MerkleTree:
    class Node:
        def __init__(self, mom, dad, hash_val):
            self.mom = mom
            self.dad = dad
            if mom == None:
                self._height = 0
            else:
                self._height = mom.height + 1

            self.hash = hash_val
            self.child = None
    
        @property
        def height(self):
            return self._height
    
        @height.setter
        def height(self,height):
            if height < 0:
                raise Exception("Attempt to set height < 0.")
            self._height = height

        def get_parent_by_spouse(self, spouse_hash):
            if spouse_hash == self.mom.hash:
                return self.dad
            return self.mom

    def __init__(self, items):
        if len(items) <= 0:
            raise Exception("items must contain at least 1" + \
                    "element for a valid merkle tree.")
        self.is_built = False
        self.root_hash = None
        self.node_table = {}
        self.max_height = math.ceil(math.log(len(items), 2))
        self.leaves = map(self._leafify, map(self._md5sum, items))

        if items and len(items) > 0:
            self.build_tree()

    def _leafify(self, data):
        leaf = self.Node(None, None, data)
        leaf.height = 0
        return leaf

    def _get_branch_by_hash(self, hash_):
        """ Returns an authentication path as a list in order from the top
            to the bottom of the tree (assumes preconditions have been checked).
        """
        path = []
        while hash_ != self.root_hash:
            node = self.node_table[hash_]
            child = node.child
            spouse = child.get_parent_by_spouse(hash_)
            path.append(spouse.hash)
            hash_ = child.hash

        path.append(hash_)
        path.reverse()
        return path
    
    def _md5sum(self, data):
        """ Returns an md5 hash of data. 
            If data is a file it is expected to contain its full path.
        """
        data = str(data)
        m = hashlib.md5()
        if os.path.isfile(data):
            try:   
                f = file(data, 'rb')
            except:
                return 'ERROR: unable to open %s' % data
            while True:
                d = f.read(8096)
                if not d:
                    break
                m.update(d)
            f.close()
        # Otherwise it could be either 1) a directory 2) miscellaneous data (like json)
        else:
            m.update(data)
        return m.hexdigest()

    def _audit(self, questioned_hash, proof_hashes):
        """ Tests if questioned_hash is a member of the merkle tree by
            hashing it with its sibling until the root hash is reached. 
        """
        proof_hash = proof_hashes.pop()

        if not proof_hash in self.node_table.keys():
            return False

        sibling = self.node_table[proof_hash]
        child = sibling.child

        # Because the order in which the hashes are concatenated matters,
        # we must test to see if questioned_hash is the "mother" or "father"
        # of its child (the hash is always build as mother + father).
        if child.mom.hash == questioned_hash:
            actual_hash = self._md5sum(questioned_hash + sibling.hash)
        elif child.dad.hash == questioned_hash:
            actual_hash = self._md5sum(sibling.hash + questioned_hash)
        else:
            return False

        if actual_hash != child.hash:
            return False
        if actual_hash == self.root_hash:
            return True

        return self._audit(actual_hash, proof_hashes)

    def _handle_solo_node_case(self,):
        # The earlier method for building the tree will fail in a one node case
        if len(self.leaves) == 1:
            solo_node = self.leaves.pop()
            self.root_hash = solo_node.hash
            self.node_table[solo_node.hash] = solo_node

    def _get_leaf_hashes(self):
        return [node.hash for node in self.node_table.values() if node.mom == None]

    # TODO break into sub methods?
    def build_tree(self):
        """ Builds a merkle tree by adding leaves one at a time to a stack,
            and combining leaves in the stack when they are of the same height.
            Expected items to be an array of type Node.
            Also constructs node_table, a dict containing hashes that map to 
            individual nodes for auditing purposes.
        """
        stack = []
        self._handle_solo_node_case()
        while self.root_hash == None:
            if len(stack) >= 2 and stack[-1].height == stack[-2].height:
                mom = stack.pop()
                dad = stack.pop()
                child_hash = self._md5sum(mom.hash + dad.hash)
                child = self.Node(mom, dad, child_hash)
                self.node_table[child_hash] = child
                mom.child = child
                dad.child = child

                if child.height == self.max_height:
                    self.root_hash = child.hash

                stack.append(child)
            elif len(self.leaves) > 0:
                leaf = self.leaves.pop()
                self.node_table[leaf.hash] = leaf
                stack.append(leaf)
            # Handle case where last 2 nodes do not match in height by "graduating"
            # last node
            else:
                stack[-1].height += 1
        self.is_built = True

    def audit(self, data, proof_hashes):
        """ Returns a boolean testing if a data (a file or object)
            is contained in the merkle tree. 

            proof_hashes are the nodes to hash the hash of data with 
            in order from the bottom of the tree to the second-to-last
            level. len(proof_hashes) is expected to be the height of the
            tree, ceil(log2(n)), as one node is needed for proof per layer.

            If the tree has not been built, returns False for any data.
        """
        if self.root_hash == None:
            return False

        hash_ = self._md5sum(data)

        # A one element tree does not make much sense, but if one exists
        # we simply need to check if the files hash is the correct root
        if self.max_height == 0 and hash_ == self.root_hash:
            return True
        if self.max_height == 0 and hash_ != self.root_hash:
            return False

        proof_hashes_cp = copy.copy(proof_hashes)
        return self._audit(hash_, proof_hashes_cp)
    
    def get_branch(self, item):
        """ Returns an authentication path for an item (not hashed) in 
            the Merkle tree as a list in order from the top of the tree
            to the bottom.
        """
        if not self.is_built:
            raise Exception("The Merkle Tree must be built before an \
                    authentication path is found.")

        hash_ = self._md5sum(item)

        if not hash_ in self._get_leaf_hashes():
            raise Exception("The requested item is not in the merkle tree.")

        return self._get_branch_by_hash(hash_)


