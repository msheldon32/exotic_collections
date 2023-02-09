from collections import defaultdict, namedtuple, deque
import regex as re

class BijectiveDict(dict):
    """
        A dictionary that is bijective, and therefore can be accessedboth forwards and backwards.
    """
    def __init__(self, *args, **kwargs):
        super(BijectiveDict, self).__init__(*args, **kwargs)
        self.inverse = dict(zip(self.values(), self.keys()))

    def __getitem__(self, key):
        return super(BijectiveDict, self).__getitem__(key)

    def __setitem__(self, key, value):
        if value in self.inverse and self.inverse[value] != key:
            raise ValueError("Value already exists")
        if key in self:
            del self.inverse[self[key]]
        super(BijectiveDict, self).__setitem__(key, value)
        self.inverse[value] = key

    def __delitem__(self, key):
        value = self[key]
        super(BijectiveDict, self).__delitem__(key)
        del self.inverse[value]

    def __repr__(self):
        return super(BijectiveDict, self).__repr__() + ""

    def __delitem__(self, key):
        val = self[key]
        super(BijectiveDict, self).__delitem__(key)
        del self.inverse[val]


class KDepthDict(dict):
    """
       A dictionary with a fixed depth of k.
    """
    def __init__(self, k_depth, *args, **kwargs):
        super(KDepthDict, self).__init__(*args, **kwargs)
        self.k_depth = k_depth

    @classmethod
    def from_dict(cls, dictionary, k_depth):
        kdepth_dict = cls(k_depth)
        if k_depth == 0:
            raise KeyError("Cannot set a value at depth 0")

        for key, value in dictionary.items():
            if k_depth == 1 and isinstance(value, dict):
                raise KeyError("Cannot set a dictionary at depth 1")
            elif k_depth > 1 and isinstance(value, dict):
                kdepth_dict[key] = cls.from_dict(value, k_depth - 1)
            elif k_depth > 1 and not isinstance(value, dict):
                raise KeyError("Cannot set a non-dictionary value at depth {}".format(k_depth))
            kdepth_dict[key] = value

        return kdepth_dict

    def __getitem__(self, key):
        if isinstance(key, tuple) or isinstance(key, list):
            if len(key) != self.k_depth:
                raise KeyError("Key of length {} does not match depth {}".format(len(key), self.k_depth))
            dic_iter = self
            for k in key:
                dic_iter = dic_iter[k]
            return dic_iter

        if key in self:
            return super(KDepthDict, self).__getitem__(key)
        else:
            self[key] = KDepthDict(self.k_depth - 1)
            self[key].k_depth = self.k_depth - 1
            return self[key]

    def __repr__(self):
        return super(KDepthDict, self).__repr__() + ""

    def __setitem__(self, key, value):
        if self.k_depth == 0:
            raise KeyError("Cannot set a value at depth 0")
        elif self.k_depth == 1:
            if isinstance(value, dict):
                raise KeyError("Cannot set a dictionary at depth 1")
            super(KDepthDict, self).__setitem__(key, value)
        else:
            if isinstance(value, KDepthDict):
                if value.k_depth != self.k_depth - 1:
                    raise KeyError("Cannot set a dictionary of depth {} at depth {}".format(value.k_depth, self.k_depth))
                super(KDepthDict, self).__setitem__(key, value)
            elif isinstance(value, dict):
                kdepth_dict = KDepthDict.from_dict(value, self.k_depth - 1)
                super(KDepthDict, self).__setitem__(key, kdepth_dict)
            else:
                raise KeyError("Cannot set a non-dictionary value at depth {}".format(self.k_depth))


class AccessCountDict(dict):
    """
        A dictionary that keeps track of the number of reads and writes to each element
    """
    def __init__(self, *args, **kwargs):
        super(AccessCountDict, self).__init__(*args, **kwargs)
        self.access_count = defaultdict(int)
        self.write_count = defaultdict(int)

    def __getitem__(self, key):
        self.access_count[key] += 1
        return super(AccessCountDict, self).__getitem__(key)

    def __setitem__(self, key, value):
        self.write_count[key] += 1
        super(AccessCountDict, self).__setitem__(key, value)

    def __delitem__(self, key):
        self.write_count[key] += 1
        super(AccessCountDict, self).__delitem__(key)

    def __add__(self, other):
        if not isinstance(other, AccessCountDict):
            raise ValueError("Cannot add a non-AccessCountDict object")

        # create a union of both self and other
        new_dict = AccessCountDict()
        for key, value in self.items():
            new_dict[key] = value
        for key, value in other.items():
            new_dict[key] = value

        # reset, and then add access/write counts accordingly
        for key, value in self.access_count.items():
            new_dict.access_count[key] = value
            new_dict.write_count[key] = self.write_count[key]

        for key, value in other.access_count.items():
            new_dict.access_count[key] += value
            new_dict.write_count[key] += other.write_count[key]

        return new_dict
    
    def __repr__(self):
        return super(AccessCountDict, self).__repr__() + ""

class BFSIter:
    """
        A class that implements a breadth-first search iterator
    """
    def __init__(self, root, child_attribute="__iter__", use_seen=True, max_depth=None):
        self.child_attribute = child_attribute
        self.is_child_callable = False
        
        if self.child_attribute != "__iter__":
            if not hasattr(root, self.child_attribute):
                raise ValueError("Root does not have attribute {}".format(self.child_attribute))
            self.is_child_callable = callable(getattr(root, self.child_attribute))

            if not hasattr(getattr(root, self.child_attribute), "__iter__") and not self.is_child_callable:
                raise ValueError("Attribute {} of root is not iterable".format(self.child_attribute))

        self.deque = deque([(0,root)])
        if use_seen:
            self.seen = set([root])
        self.use_seen = use_seen
        self.max_depth = max_depth

        self.orig_root = root

    def reset(self):
        self.deque = deque([(0,self.orig_root)])
        if self.use_seen:
            self.seen = set([self.orig_root])

    def pop(self):
        return self.__next__()

    def __next__(self):
        if len(self.deque) == 0:
            raise StopIteration
        res = self.deque.popleft()

        if self.child_attribute == "__iter__":
            if not hasattr(res[1], "__iter__"):
                return res
            neighbors = [x for x in res[1]]
        elif self.is_child_callable:
            neighbors = getattr(res[1], self.child_attribute)()
        else:
            neighbors = [x for x in getattr(res[1], self.child_attribute)]

        for neighbor in neighbors:
            if self.use_seen and neighbor in self.seen:
                continue
            if self.max_depth is not None and res[0] >= self.max_depth:
                continue
            self.deque.append((res[0]+1, neighbor))
            if self.use_seen:
                self.seen.add(neighbor)
        return res

    def __iter__(self):
        return self

class DFSIter:
    """
        A class that implements a depth-first search iterator
    """
    def __init__(self, root, child_attribute="__iter__", use_seen=True, max_depth=None):
        self.child_attribute = child_attribute
        self.is_child_callable = False
        
        if self.child_attribute != "__iter__":
            if not hasattr(root, self.child_attribute):
                raise ValueError("Root does not have attribute {}".format(self.child_attribute))
            self.is_child_callable = callable(getattr(root, self.child_attribute))

            if not hasattr(getattr(root, self.child_attribute), "__iter__") and not self.is_child_callable:
                raise ValueError("Attribute {} of root is not iterable".format(self.child_attribute))

        self.deque = deque([(0,root)])
        if use_seen:
            self.seen = set([root])
        self.use_seen = use_seen
        self.max_depth = max_depth
        self.orig_root = root

    def pop(self):
        return self.__next__()

    def __next__(self):
        if len(self.deque) == 0:
            raise StopIteration

        res = self.deque.pop()

        if self.child_attribute == "__iter__":
            if not hasattr(res[1], "__iter__"):
                return res
            neighbors = [x for x in res[1]]
        elif self.is_child_callable:
            neighbors = getattr(res[1], self.child_attribute)()
        else:
            neighbors = [x for x in getattr(res[1], self.child_attribute)]

        for neighbor in neighbors:
            if self.use_seen and neighbor in self.seen:
                continue
            if self.max_depth is not None and res[0] >= self.max_depth:
                continue
            self.deque.append((res[0]+1, neighbor))
            if self.use_seen:
                self.seen.add(neighbor)
        return res

    def reset(self):
        self.deque = deque([(0,self.orig_root)])
        if self.use_seen:
            self.seen = set([self.orig_root])

    def __iter__(self):
        return self


class TrieNode:
    def __init__(self, char):
        self.char = char
        self.children = {}
        self.is_end = False

    def __repr__(self):
        return "TrieNode({})".format(self.char)

class Trie:
    def __init__(self):
        self.root = TrieNode(None)

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode(char)
            node = node.children[char]
        node.is_end = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def __repr__(self):
        return "Trie({})".format(self.root)
    
