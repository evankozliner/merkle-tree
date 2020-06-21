# Merkle Tree

This is an educational project that shows a basic Merkle Tree implementation. 

1. Accompanies [this blog post](https://medium.com/@evankozliner/merkle-tree-introduction-4c44250e2da7) where the concept is fleshed out in detail.
2. In not intended for production use cases. There are more high-end ways to traverse the tree than what is presented here. Read the below paper for some examples. 
3. Implementation built from the following paper: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.84.9700&rep=rep1&type=pdf


## Running this project and testing

```
% git checkout https://github.com/evankozliner/merkle-tree.git
% cd merkle-tree


% python MerkleTreeTest.py
..........
----------------------------------------------------------------------
Ran 10 tests in 0.002s

OK

% python FileUsageTest.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.003s

OK
```

### Quick note on Python version

I've upgraded the version on this package to Python 3. I've tested under Python
3.6.10. 

### Changelog

```
2020/06/21 - More refactoring, comments, illustrate example traversal
2020/06/20 - Moves package to Python 3. Begins refactoring for typing / better documentation
2017/09/13 - Initial creation of package
```

