import sys

sys.path.append('..')

import pytest
import random

from exotic_collections import *


@pytest.fixture
def empty_bijective_dict():
    return BijectiveDict()

@pytest.fixture
def bijective_dict():
    return BijectiveDict({1: 'a', 2: 'b', 3: 'c'})

@pytest.fixture
def random_bijective_dict():
    keys = [random.randint(0, 1000) for _ in range(10)]
    values = [random.randint(0, 1000) for _ in range(10)]

    keys = list(set(keys))
    values = list(set(values))

    if len(keys) > len(values):
        keys = keys[:len(values)]

    if len(values) > len(keys):
        values = values[:len(keys)]

    return [BijectiveDict({k: v for k, v in zip(keys, values)}), keys, values]

def test_bijective_dict_init(empty_bijective_dict):
    assert len(empty_bijective_dict) == 0
    assert empty_bijective_dict == {}

def test_bijective_dict_init_with_dict(bijective_dict):
    assert len(bijective_dict) == 3
    assert bijective_dict == {1: 'a', 2: 'b', 3: 'c'}

def test_bijective_dict_setitem(bijective_dict):
    bijective_dict[4] = 'd'
    assert len(bijective_dict) == 4
    assert bijective_dict == {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
    assert bijective_dict.inverse == {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    assert bijective_dict[4] == 'd'
    assert bijective_dict.inverse['d'] == 4

def test_bijective_dict_setitem_with_existing_key(bijective_dict):
    bijective_dict[1] = 'd'
    assert len(bijective_dict) == 3
    assert bijective_dict == {1: 'd', 2: 'b', 3: 'c'}
    assert bijective_dict.inverse == {'d': 1, 'b': 2, 'c': 3}
    assert bijective_dict[1] == 'd'
    assert bijective_dict.inverse['d'] == 1

def test_bijective_dict_setitem_with_existing_value(bijective_dict):
    with pytest.raises(ValueError):
        bijective_dict[4] = 'a'

def test_bijective_dict_delitem(bijective_dict):
    del bijective_dict[1]
    assert len(bijective_dict) == 2
    assert bijective_dict == {2: 'b', 3: 'c'}
    assert bijective_dict.inverse == {'b': 2, 'c': 3}

def test_bijective_dict_delitem_with_non_existing_key(bijective_dict):
    with pytest.raises(KeyError):
        del bijective_dict[4]

def test_bijective_dict_delitem_with_non_existing_value(bijective_dict):
    with pytest.raises(KeyError):
        del bijective_dict.inverse['d']

def test_bijective_dict_random(random_bijective_dict):
    bijective_dict, keys, values = random_bijective_dict

    assert len(bijective_dict) == len(keys)
    assert len(bijective_dict.inverse) == len(values)

    for key, value in zip(keys, values):
        assert bijective_dict[key] == value
        assert bijective_dict.inverse[value] == key

def test_bijective_dict_random_with_existing_key(random_bijective_dict):
    bijective_dict, keys, values = random_bijective_dict

    key = keys[0]
    value = values[0]

    bijective_dict[key] = value

    assert len(bijective_dict) == len(keys)
    assert len(bijective_dict.inverse) == len(values)

    for key, value in zip(keys, values):
        assert bijective_dict[key] == value
        assert bijective_dict.inverse[value] == key

def test_bijective_dict_random_with_existing_value(random_bijective_dict):
    bijective_dict, keys, values = random_bijective_dict

    key = random.randint(1001, 2000)
    value = values[0]

    with pytest.raises(ValueError):
        bijective_dict[key] = value

def test_bijective_dict_random_with_existing_key_and_value(random_bijective_dict):
    bijective_dict, keys, values = random_bijective_dict

    key = keys[0]
    value = values[0]

    bijective_dict[key] = value
    bijective_dict[key] = value

    assert len(bijective_dict) == len(keys)
    assert len(bijective_dict.inverse) == len(values)

    for key, value in zip(keys, values):
        assert bijective_dict[key] == value
        assert bijective_dict.inverse[value] == key


