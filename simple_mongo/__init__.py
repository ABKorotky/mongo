#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

from bson.objectid import ObjectId
from connection import MongoClientConnection
import exceptions


class MongoDatabase(object):

    _conn = None
    _db = None

    def __init__(self, database, **kwargs):
        self.use_connection(**kwargs)
        self._db = database

    def __str__(self):
        return u'The Mongo "%s" database' % self._db

    def use_connection(self, **kwargs):
        '''
        override this method for change Mongo Connection class/object
        '''
        self._conn = MongoClientConnection(**kwargs)

    @property
    def connection(self):
        return self._conn

    @property
    def db(self):
        #return self._conn[self._db]
        return getattr(self.connection, self._db)

    def _prepare_id(self, _id):
        if isinstance(_id, ObjectId):
            return _id
        elif isinstance(_id, basestring) or isinstance(_id, int):
            return ObjectId(_id)
        else:
            return None

    def __getattr__(self, item):
        if hasattr(self.db, item):
            return getattr(self.db, item)
        raise AttributeError(u'The Mongo Database object hasn`t "%s" attribute'\
                             % item)


# short alias
MDB = MongoDatabase