#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

from simple_mongo import MDB
from simple_mongo.document import MDoc
from simple_mongo.cursor import MCur


__all__ = ['MongoCollection', 'MC']


class MongoCollection(MDB):

    _collection = None

    def __init__(self, database, collection, **kwargs):
        super(MongoCollection, self).__init__(database, **kwargs)
        self._collection = collection

    def __str__(self):
        return u'The Mongo "%s.%s" collection' % (self._db, self._collection)

    @property
    def collection(self):
        if self._db is not None:
            return getattr(self.db, self._collection)
        else:
            return None

    def __len__(self):
        if self.collection is not None:
            return self.collection.count()
        else:
            return 0

    def find(self, query={}, fields=None, *args, **kwargs):
        if isinstance(fields, list) or isinstance(fields, tuple):
            cursor = self.collection.find(query, fields)
        else:
            cursor = self.collection.find(query)
        return MCur(cursor)

    def create_doc(self, doc, **kwargs):
        _id = self.collection.insert(doc, **kwargs)
        return MDoc(_id=_id, collection=self.collection)

    def create_empty_doc(self, **kwargs):
        return self.create_doc({}, **kwargs)


# short alias
MC = MongoCollection