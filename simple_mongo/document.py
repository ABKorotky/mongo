#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from simple_mongo import MDB


class MongoDocument(MDB):

    _collection = None
    _doc = None
    _xid = None

    def __init__(self, database, collection, *args, **kwargs):
        super(MongoDocument, self).__init__(database, **kwargs)
        self._collection = collection
        #TODO - insert initialisation document functionality

    def __str__(self):
        if self._xid:
            return u'The Mongo <%s> document from "%s.%s" collection' % (self._xid, self._db, self._collection)
        else:
            return u'The not initialized Mongo document from "%s.%s" collection' % (self._db, self._collection)


# short alias
MDoc = MongoDocument