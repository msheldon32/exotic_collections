import sys

sys.path.append('..')

import pytest
import random

from exotic_collections import *


@pytest.fixture
def kdepth_dict():
    return KDepthDict(3)

@pytest.fixture
def kdepth_dict_with_data():
    return KDepthDict(3, {'a': {'b': {'c': 1}}})

def test_kdepth_dict_init(kdepth_dict, kdepth_dict_with_data):
    assert kdepth_dict.k_depth == 3
    assert kdepth_dict == {}

    assert kdepth_dict_with_data.k_depth == 3
    assert kdepth_dict_with_data == {'a': {'b': {'c': 1}}}

def test_kdepth_dict_setitem(kdepth_dict):
    kdepth_dict['a']['b'] = {}
    assert kdepth_dict == {'a': {'b': {}}}

    kdepth_dict['a']['b'] = {'c': 1}
    assert kdepth_dict == {'a': {'b': {'c': 1}}}

    kdepth_dict['a']['b']['c'] = 3
    assert kdepth_dict == {'a': {'b': {'c': 3}}}
    
    with pytest.raises(KeyError):
        kdepth_dict['a'] = 1
        kdepth_dict['a']['b'] = 2
        kdepth_dict['a']['b']['c']['d'] = 4
        kdepth_dict['a']['b']['c']['d']['e'] = 5

def test_kdepth_dict_getitem(kdepth_dict_with_data):
    assert kdepth_dict_with_data['a']['b']['c'] == 1

def test_kdepth_dict_delitem(kdepth_dict_with_data):
    del kdepth_dict_with_data['a']['b']['c']
    assert kdepth_dict_with_data == {'a': {'b': {}}}

    with pytest.raises(KeyError):
        del kdepth_dict_with_data['a']['b']['c']
