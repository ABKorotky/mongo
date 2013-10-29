#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from bson.objectid import ObjectId
from simple_mongo import MDB
import exceptions
from utils import map_dict


__all__ = ['MongoDocument', 'MDoc']


class MongoDocument(MDB):

    _collection = None
    _doc = None
    _id = None
    _map = None

    def __init__(self, _id=None, doc=None, **kwargs):
        if not _id:
            if isinstance(doc, dict):
                _id = doc.pop('_id', None)
        self._id = self._prepare_id(_id)
        if not self._id:
            doc = doc or {}
        self._prepare_doc(doc)
        self._collection = kwargs.pop('collection', None)
        if self._collection:
            self._db = self._collection.database

    def _prepare_doc(self, doc):
        self._map = {}
        if isinstance(doc, dict):
            self._doc = map_dict(**doc)
            self._doc._map = self._map

    def load(self):
        if self._id:
            if not self._collection:
                raise exceptions.MongoException(
                    err_num=exceptions.COLLECTION_MISSING)
            doc = self._collection.find_one({'_id': self._id}) or {}
            self._prepare_doc(doc)
        else:
            raise exceptions.MongoException(
                err_num=exceptions.DOCUMENT_LOAD_ERROR)

    def as_dict(self):
        return self._doc if self._doc else {}

    def save(self, **kwargs):
        if self._id:
            if self._map:
                self._collection.update({'_id': self._id}, self._map, **kwargs)
                self._map = {}
                return True
            return False
        else:
            _id = self._collection.insert(self._doc, **kwargs)
            self._id = self._prepare_id(_id)
            self._map = {}

    def __getitem__(self, item):
        if self._doc is None:
            self.load()
        return self._doc[item]

    def __setitem__(self, key, value):
        if self._doc is None:
            self.load()
        self._doc[key] = value

    def __delitem__(self, key):
        if self._doc is None:
            self.load()
        del self._doc[key]

    def __str__(self):
        return str(self._doc)

    def __getattr__(self, item):
        if self._doc is None:
            self.load()
        if hasattr(self._doc, item):
            return getattr(self._doc, item)
        raise AttributeError(u'The "%s" instance has not "%s" attribute' %
                                 (self.__class__.__name__, item))


# short alias
MDoc = MongoDocument