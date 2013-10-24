#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

from simple_mongo import MDB


class MongoCollection(MDB):

    _collection = None

    def __init__(self, database, collection, **kwargs):
        super(MongoCollection, self).__init__(database, **kwargs)
        self._collection = collection

    def __str__(self):
        return u'The Mongo "%s.%s" collection' % (self._db, self._collection)

    @property
    def collection(self):
        if self.db is not None:
            return getattr(self.db, self._collection)
        else:
            return None

    def __len__(self):
        if self.collection is not None:
            return self.collection.find({}).count()
        else:
            return 0


# short alias
MC = MongoCollection