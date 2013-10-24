#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from simple_mongo import MDB, MongoException


__all__ = ['MongoDocument', 'MDoc']


class MDocException(MongoException):

    def __init__(self, **kwargs):
        number = kwargs.pop('number', 10)
        msg = kwargs.pop('msg', 'The basic Mongo Document Exception')
        super(MDocException, self).__init__(number=number, msg=msg)


class MDocLoadException(MDocException):

    def __init__(self, _id):
        super(MDocException, self).__init__(number=11, msg='The Mongo Document with _id=<%s> does not be loaded: collection is None' % _id)


class MongoDocument(MDB):

    _collection = None
    _doc = None
    _xid = None

    def __init__(self, **kwargs):
        self._xid = kwargs.pop('_id', None)
        self._doc = kwargs.pop('doc', None)
        if self._doc and '_id' in self._doc:
            self._xid = self._doc['_id']
        self._collection = kwargs.pop('collection', None)
        if self._collection:
            self._db = self._collection.database

    def load(self):
        if not self._collection:
            raise MDocLoadException(self._xid)
        self._doc = self._collection.find_one({'_id': self._xid})

    def __str__(self):
        if self._xid:
            return u'The Mongo <%s> document from "%s.%s" collection' % (self._xid, self._db.name, self._collection.name)
        else:
            return u'The not initialized Mongo document '

    def __getattr__(self, item):
        if self._doc is None:
            self.load()
        if hasattr(self._doc, item):
            return getattr(self._doc, item)
        raise AttributeError(u'The Mongo Document has not "%s" attribute' % item)


# short alias
MDoc = MongoDocument