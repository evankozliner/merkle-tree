from typing import *

# TODO typing everywhere
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

