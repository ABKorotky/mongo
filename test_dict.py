#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


OP_SET = 'set'
OP_APPEND = 'append'
OP_DELETE = 'del'
OP_CHANGE = 'change'


class map_dict(dict):

    _map = None

    def set_map(self, _map):
        self._map = _map

    def get_map(self):
        return self._map

    def __getitem__(self, item):
        val = super(map_dict, self).__getitem__(item)
        if not self._map.has_key(item):
            map_val = map_factory(val)
            if map_val:
                self._map[item] = {}
                self.origin_setitem(item, map_val)
                self[item].set_map(self._map[item])
                return map_val
        return val

    def origin_setitem(self, key, value):
        super(map_dict, self).__setitem__(key, value)

    def __setitem__(self, key, value):
        self._map[key] = OP_CHANGE
        if not key in self:
            self._map[key] = OP_SET
        super(map_dict, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(map_dict, self).__delitem__(key)
        self._map[key] = OP_DELETE


class map_list(list):

    _map = None

    def set_map(self, _map):
        self._map = _map

    def get_map(self):
        return self._map

    def __getitem__(self, item):
        val = super(map_list, self).__getitem__(item)
        if not self._map.has_key(item):
            map_val = map_factory(val)
            if map_val:
                self._map[item] = {}
                self.origin_setitem(item, map_val)
                self[item].set_map(self._map[item])
                return self[item]
        return val

    def origin_setitem(self, key, value):
        super(map_list, self).__setitem__(key, value)

    def __setitem__(self, key, value):
        self._map[key] = OP_CHANGE
        if not key in self:
            self._map[key] = OP_APPEND
        super(map_list, self).__setitem__(key, value)

    def __delitem__(self, key):
        super(map_list, self).__delitem__(key)
        self._map[key] = OP_DELETE


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
        'k3': "AlekSS",
        'k4': [12, 13, 14],
        'k5': {
            'k51': False,
            'k52': [21, 22, 23],
            'k53': {
                'k531': 'Level 3 key'
            },
        },
    })
    d.set_map(_map)
    print "map before edit: %s" % _map
    print "key before edit: %s" % d['k5']['k53']['k531']
    print "============================================"
    d['k5']['k53']['k531'] = 'level 3 key edit'
    d['k5']['k53']['k532'] = 'new key'
    d['k6'] = 'new key too'
    d['k4'][1] = 3333
    d['k4'].append(5555)
    d['k4'].insert(1, 7777)
    del d['k4'][0]
    del d['k5']['k52']
    print "============================================"
    print "key after edit: %s" % d['k5']['k53']['k531']
    print "map after edit: %s" % _map
    print d


if __name__ == '__main__':
    main()