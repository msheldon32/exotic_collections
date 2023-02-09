import sys

sys.path.append('..')

import pytest
import random

from exotic_collections import *


@pytest.fixture
def access_count_dict():
    return AccessCountDict()

@pytest.fixture
def access_count_dict_with_data():
    return AccessCountDict({'a': 1, 'b': 2, 'c': 3})

def test_access_count_dict_init(access_count_dict):
    assert access_count_dict == {}

def test_access_count_dict_init_with_data(access_count_dict_with_data):
    assert access_count_dict_with_data == {'a': 1, 'b': 2, 'c': 3}

def test_access_count_dict_get(access_count_dict_with_data):
    assert access_count_dict_with_data['a'] == 1
    assert access_count_dict_with_data['b'] == 2
    assert access_count_dict_with_data['c'] == 3

    assert access_count_dict_with_data.access_count['a'] == 1
    assert access_count_dict_with_data.access_count['b'] == 1
    assert access_count_dict_with_data.access_count['c'] == 1
    assert access_count_dict_with_data.access_count == {'a': 1, 'b': 1, 'c': 1}
    assert access_count_dict_with_data.access_count['d'] == 0

    assert access_count_dict_with_data.write_count['a'] == 0
    assert access_count_dict_with_data.write_count['b'] == 0
    assert access_count_dict_with_data.write_count['c'] == 0


def test_access_count_dict_set(access_count_dict):
    access_count_dict['a'] = 1
    access_count_dict['b'] = 2
    access_count_dict['c'] = 3

    assert access_count_dict == {'a': 1, 'b': 2, 'c': 3}
    assert access_count_dict.access_count['a'] == 0
    assert access_count_dict.access_count['b'] == 0
    assert access_count_dict.access_count['c'] == 0
    assert access_count_dict.access_count == {'a': 0, 'b': 0, 'c': 0}

    assert access_count_dict.write_count['a'] == 1
    assert access_count_dict.write_count['b'] == 1
    assert access_count_dict.write_count['c'] == 1
    assert access_count_dict.write_count == {'a': 1, 'b': 1, 'c': 1}

