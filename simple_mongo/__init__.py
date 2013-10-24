#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from pymongo import Connection
from pymongo.errors import ConnectionFailure

#from collection import *
#from document import *
#from cursor import *


class MongoException(Exception):

    def __init__(self, **kwargs):
        number = kwargs.pop('number', 1)
        msg = kwargs.pop('msg', 'The basic Mondo Exception')
        self.args = (number, msg)


class MongoConnection(object):
    '''
    Wrapper class for realize 'PseudoSingleton' pattern.
    If we pass
        conn_obj = MongoConnection()
    we get a really Singleton.
    But if we pass
        conn_obj = MongoConnection(new_connection=True)
    we get a new different class.
    '''

    _conn = None

    def __new__(cls, *args, **kwargs):
        is_new = kwargs.pop('new_connection', False)
        if is_new:
            return cls._make_connection(**kwargs)
        else:
            if cls._conn is None:
                cls._conn = cls._make_connection(**kwargs)
            return cls._conn

    @staticmethod
    def _make_connection(**kwargs):
        try:
            return Connection(**kwargs)
        except ConnectionFailure:
            #TODO - insert loging functionality
            return None

# short alias
MConn = MongoConnection


class MongoDatabase(object):

    _conn = None
    _db = None

    def __init__(self, database, **kwargs):
        self._conn = MConn(**kwargs)
        self._db = database

    def __str__(self):
        return u'The Mongo "%s" database' % self._db

    @property
    def db(self):
        if self._conn is not None:
            return self._conn[self._db]
        else:
            return None


# short alias
MDB = MongoDatabase