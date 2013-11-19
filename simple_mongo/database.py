#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from connection import DefaultConnection
from collection import Collection


class Database(object):

    _conn = None
    _collection_map = None
    db = None

    def __init__(self, db_name, **kwargs):
        self._collection_map = kwargs.pop('collection_map', None)
        conn = kwargs.pop('connection', DefaultConnection)
        self._conn = conn(**kwargs)
        self.db = self._conn[db_name]

    def __str__(self):
        return u'The Mongo "%s" database' % self.db.name

    @property
    def connection(self):
        return self._conn

    def get_collection(self, name):
        if isinstance(self._collection_map, dict) and self._collection_map.has_key(name):
            return self._collection_map[name](name, self)
        else:
            return Collection(name, self)

    def __getitem__(self, item):
        '''
        Use a dictionary interface for get a wrapped mongo collections instances
        '''
        return self.db[item]

    def __getattr__(self, item):
        '''
        Use a attribute interface for get mongo database methods
        '''
        if hasattr(self.db, item):
            return getattr(self.db, item)
        raise AttributeError(u'The Mongo Database object hasn`t "%s" attribute'\
                             % item)