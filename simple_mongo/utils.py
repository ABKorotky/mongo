#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

'''
helpers for tracking changes in dict and list data.
map_* classes wrap appropriate classes and adding to it 'track changes' functionality
'''


OP_SET = '$set'
OP_CHANGE = '$set'
OP_DELETE = '$unset'

OP_APPEND = '$push'
OP_APPEND_MANY = '$pushAll'
OP_POP = '$pop'
OP_POP_MANY = '$popAll'



class map_dict(dict):

    _map = {}
    _keys = []

    def __init__(self, **kwargs):
        super(map_dict, self).__init__(**kwargs)
        self._map = {}
        self._keys = []

    def __getitem__(self, item):
        val = super(map_dict, self).__getitem__(item)
        if not item in self._map:
            map_val = map_factory(val)
            if map_val:
                map_val._map = self._map
                map_val._keys = list(self._keys)
                map_val._keys.append(item)
                self.origin_setitem(item, map_val)
                return map_val
        return val

    def origin_setitem(self, key, value):
        super(map_dict, self).__setitem__(key, value)

    def _build_map_key(self, key):
        keys = list(self._keys)
        if key:
            keys.append(str(key))
        return '.'.join(keys)

    def __setitem__(self, key, value):
        super(map_dict, self).__setitem__(key, value)
        if OP_SET not in self._map:
            self._map[OP_SET] = {}
        self._map[OP_SET].update({self._build_map_key(key): type(value)(value)})

    def __delitem__(self, key):
        super(map_dict, self).__delitem__(key)
        if OP_DELETE not in self._map:
            self._map[OP_DELETE] = {}
        self._map[OP_DELETE].update({self._build_map_key(key): 1})

    def __getattr__(self, item):
        return super(map_dict, self).__getattr__(item)

    def __setattr__(self, key, value):
        super(map_dict, self).__setattr__(key, value)

    def __delattr__(self, item):
        super(map_dict, self).__delattr__(item)


class map_list(list):

    _map = {}
    _keys = []

    def __init__(self, *args):
        super(map_list, self).__init__(*args)
        self._map = {}
        self._keys = []

    def __getitem__(self, item):
        val = super(map_list, self).__getitem__(item)
        if not self._map.has_key(item):
            map_val = map_factory(val)
            if map_val:
                map_val._map = self._map
                map_val._keys = list(self._keys)
                map_val._keys.append(item)
                self.origin_setitem(item, map_val)
                return self[item]
        return val

    def origin_setitem(self, key, value):
        super(map_list, self).__setitem__(key, value)

    def _build_map_key(self, key):
        keys = list(self._keys)
        if key:
            keys.append(str(key))
        return '.'.join(keys)

    def __setitem__(self, key, value):
        super(map_list, self).__setitem__(key, value)
        if OP_SET not in self._map:
            self._map[OP_SET] = {}
        self._map[OP_SET].update({self._build_map_key(key): type(value)(value)})

    def __delitem__(self, key):
        k = self._build_map_key(None)
        if OP_POP_MANY not in self._map:
            self._map[OP_POP_MANY] = {}
        if k not in self._map[OP_POP_MANY]:
            self._map[OP_POP_MANY][k] = []
        self._map[OP_POP_MANY][k].append(super(map_list, self).__getitem__(key))
        super(map_list, self).__delitem__(key)

    def append(self, p_object):
        super(map_list, self).append(p_object)
        k = self._build_map_key(None)
        if OP_APPEND_MANY not in self._map:
            self._map[OP_APPEND_MANY] = {}
        if k not in self._map[OP_APPEND_MANY]:
            self._map[OP_APPEND_MANY][k] = []
        self._map[OP_APPEND_MANY][k].append(p_object)

    def insert(self, index, p_object):
        super(map_list, self).insert(index, p_object)
        k = self._build_map_key(None)
        if OP_APPEND_MANY not in self._map:
            self._map[OP_APPEND_MANY] = {}
        if k not in self._map[OP_APPEND_MANY]:
            self._map[OP_APPEND_MANY][k] = []
        self._map[OP_APPEND_MANY][k].append(p_object)

    def __getattr__(self, item):
        return super(map_list, self).__getattr__(item)

    def __setattr__(self, key, value):
        super(map_list, self).__setattr__(key, value)

    def __delattr__(self, item):
        super(map_list, self).__delattr__(item)


def map_factory(obj):
    if isinstance(obj, dict):
        return map_dict(**obj)
    elif isinstance(obj, list):
        return map_list(obj)
    return None

def main():
    _map = {}
    d = map_dict(**{
        'k1': True,
        'k2': 12,
        'k3': "Aleks",
        'k4': [12, 13, 14],
        'k5': {
            'k51': False,
            'k52': [21, 22, 23],
            'k53': {
                'k531': 'Level 3 key'
            },
        },
    })
    d._map = _map
    print "map before edit: %s" % _map
    print "key before edit: %s" % d['k5']['k53']['k531']
    print "============================================"
    d['k5']['k53']['k531'] = 'level 3 key edit'
    d['k5']['k53']['k532'] = 'new key'
    d['k6'] = 'new key too'
    d['k4'][1] = 3333
    d['k4'].append(5555)
    d['k4'].insert(1, 7777)
    d['k5']['k52'].append(5555)
    d['k5']['k52'].insert(1, 7777)
    del d['k4'][0]
    del d['k5']['k52'][0]
    print "============================================"
    print "key after edit: %s" % d['k5']['k53']['k531']
    print "map after edit: %s" % _map
    print d


if __name__ == '__main__':
    main()