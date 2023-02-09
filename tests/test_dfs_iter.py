import sys

sys.path.append('..')

import pytest
import random

from exotic_collections import *

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self):
        return str(self.value)

@pytest.fixture
def random_tree():
    N_VALUES = random.randint(1, 200)
    MAX_VALUE = 1000
    MAX_CHILDREN = 10

    def create_node(max_depth):
        node = TreeNode(random.randint(0, MAX_VALUE))
        if max_depth == 0:
            return node
        if random.random() < 0.8:
            node.children = [create_node(max_depth-1) for _ in range(random.randint(0, MAX_CHILDREN))]
        return node
    
    return create_node(5)

@pytest.fixture
def random_list_tree():
    # return a random tree within a list format
    N_VALUES = random.randint(1, 200)
    MAX_VALUE = 1000

    def generate_random_list(n_values):
        if n_values == 0:
            return []
        values_used = 0
        
        out_list = []

        while values_used < n_values:
            if random.random() < 0.5:
                n_to_add = random.randint(1, n_values - values_used)
                out_list.append(generate_random_list(n_to_add))
                values_used += n_to_add
            else:
                out_list.append(random.randint(0, MAX_VALUE))
                values_used += 1

    random_list = generate_random_list(N_VALUES)

    return random_list

def test_dfs_iter(random_list_tree):
    expected_values = []

    queue = [(0, random_list_tree)]

    while len(queue) > 0:
        depth, current = queue.pop(0)
        for child in current.children:
            if child is None:
                continue
            queue.append((depth + 1, child))
        expected_values.append((depth, current))

    for a,b in zip(DFSIter(random_list_tree, use_seen=False), expected_values):
        assert a == b

def test_dfs_iter_random(random_tree):
    expected_values = []

    queue = [(0, random_tree)]

    while len(queue) > 0:
        depth, current = queue.pop(0)
        for child in current.children:
            queue.append((depth + 1, child))
        expected_values.append((depth, current))

    for a,b in zip(DFSIter(random_tree,use_seen=False,child_attribute="children"), expected_values):
        assert a == b
