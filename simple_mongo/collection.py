#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

from bson.objectid import ObjectId
from simple_mongo import MDB, MongoException
from simple_mongo.document import MDoc
from simple_mongo.cursor import MCur


__all__ = ['MongoCollection', 'MC']


class MongoCollectionException(MongoException):

    def __init__(self, **kwargs):
        number = kwargs.pop('number', 10)
        msg = kwargs.pop('msg', 'The basic Mondo Collection Exception')
        self.args = (number, msg)


class MongoCollection(MDB):

    _collection = None

    def __init__(self, database, collection, **kwargs):
        super(MongoCollection, self).__init__(database, **kwargs)
        self._collection = collection

    def __str__(self):
        return u'The Mongo "%s.%s" collection' % (self._db, self._collection)

    @property
    def collection(self):
        return getattr(self.db, self._collection)

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

    def find_doc(self, _id=None, query=None):
        if isinstance(_id, basestring):
            _id = ObjectId(_id)
        if isinstance(_id, ObjectId):
            doc = self.collection.find_one({'_id': _id})
            return MDoc(doc=doc, collection=self.collection)
        elif isinstance(query, dict):
            doc = self.collection.find_one(query)
            return MDoc(doc=doc, collection=self.collection)
        else:
            raise AttributeError(u'The both named parameters "_id" and "query" \
            in Collection.find_doc() method can not be None')


# short alias
MC = MongoCollection