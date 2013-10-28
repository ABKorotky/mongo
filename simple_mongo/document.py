#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from bson.objectid import ObjectId
from simple_mongo import MDB, MongoException
from simple_mongo.utils import map_factory, map_dict, map_list


__all__ = ['MongoDocument', 'MDoc']


class MDocException(MongoException):

    def __init__(self, **kwargs):
        number = kwargs.pop('number', 10)
        msg = kwargs.pop('msg', 'The basic Mongo Document Exception')
        super(MDocException, self).__init__(number=number, msg=msg)


class MDocLoadException(MDocException):

    def __init__(self, _id):
        super(MDocException, self).__init__(number=11,
            msg='The Mongo Document with _id=<%s> does not be loaded: \
            collection is None' % _id)


class MongoDocument(MDB):

    _collection = None
    _doc = None
    _xid = None
    _map = None

    def __init__(self, **kwargs):
        _xid = kwargs.pop('_id', None)
        if isinstance(_xid, basestring):
            self._xid = ObjectId(_xid)
        elif isinstance(_xid, ObjectId):
            self._xid = _xid
        else:
            self._xid = None
        self._map = {}
        _doc = kwargs.pop('doc', None)
        if isinstance(_doc, dict):
            self._doc = map_dict(**_doc)
            self._doc._map = self._map
            if '_id' in self._doc:
                self._xid = self._doc['_id']
        self._collection = kwargs.pop('collection', None)
        if self._collection:
            self._db = self._collection.database

    def load(self):
        if not self._collection:
            raise MDocLoadException(self._xid)
        _doc = self._collection.find_one({'_id': self._xid})
        if isinstance(_doc, dict):
            self._doc = map_dict(_doc)
            self._doc._map = self._map

    def as_dict(self):
        return self._doc if self._doc else {}

    def save(self):
        if self._xid:
            #self._doc['_id'] = ObjectId(self._doc['_id'])
            self._collection.update({'_id': self._xid}, self._map)
            self._map = {}
            return True
        else:
            try:
                self._collection.save(self._doc)
                return True
            except TypeError:
                return False

    def refresh(self):
        self._doc = self._collection.find_one({'_id': self._xid})
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
        raise AttributeError(u'The Mongo Document hasn`t "%s" attribute' % item)


# short alias
MDoc = MongoDocument