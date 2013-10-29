#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

from bson.objectid import ObjectId
from simple_mongo import MDB
from document import MDoc
from cursor import MCur


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
        return getattr(self.db, self._collection)

    def __len__(self):
        if self.collection is not None:
            return self.collection.count()
        else:
            return 0

    def get_document_class(self):
        return MDoc

    def get_cursor_class(self):
        return MCur

    def find(self, query={}, fields=None, *args, **kwargs):
        if isinstance(fields, list) or isinstance(fields, tuple):
            cursor = self.collection.find(query, fields)
        else:
            cursor = self.collection.find(query)
        return self.get_cursor_class()(cursor)

    def create_doc(self, doc, **kwargs):
        _id = self.collection.insert(doc, **kwargs)
        return self.get_document_class()(_id=_id, doc=doc,
                                         collection=self.collection)

    def create_empty_doc(self, **kwargs):
        return self.create_doc({}, **kwargs)

    def find_doc(self, _id=None, query=None, **kwargs):
        doc = None
        if _id:
            doc = self.collection.find_one({'_id': self._prepare_id(_id)},
                                           **kwargs)
        elif isinstance(query, dict):
            doc = self.collection.find_one(query, **kwargs)
        else:
            raise AttributeError(u'The both named parameters "_id" and "query" \
            in Collection.find_doc() method can not be None')
        if doc:
            return self.get_document_class()(doc=doc,
                                             collection=self.collection)
        else:
            return None

    def find_or_create(self, _id=None, query=None, doc=None, **kwargs):
        if not _id:
            if isinstance(doc, dict):
                _id = doc.get('_id', None)
        found_doc = None
        if _id:
            found_doc = self.collection.find_one({'_id': self._prepare_id(_id)},
                                                 **kwargs)
        elif isinstance(query, dict):
            found_doc = self.collection.find_one(query, **kwargs)
        if found_doc:
            return self.get_document_class()(doc=found_doc,
                                             collection=self.collection)
        else:
            return self.create_doc(doc, **kwargs)

    def __getattr__(self, item):
        if hasattr(self.collection, item):
            return getattr(self.collection, item)
        else:
            raise AttributeError(u'The "%s" instance has not "%s" attribute' %
                                 (self.__class__.__name__, item))


# short alias
MC = MongoCollection