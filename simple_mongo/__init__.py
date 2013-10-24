#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoException(Exception):

    def __init__(self, **kwargs):
        number = kwargs.pop('number', 1)
        msg = kwargs.pop('msg', 'The basic Mondo Exception')
        self.args = (number, msg)


class MongoConnectionException(MongoException):

    def __init__(self):
        super(MongoConnectionException, self).__init__(number=2,
            msg=u'Unable to create Mongo Connection. You have errors.')

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
            return MongoClient(**kwargs)
        except ConnectionFailure:
            MongoConnection.logging()
            raise MongoConnectionException()

    @staticmethod
    def logging():
        '''
        override this method for adding logging functionality
        '''
        pass


# short alias
MConn = MongoConnection


class MongoDatabase(object):

    _conn = None
    _db = None

    def __init__(self, database, **kwargs):
        self.make_connection(**kwargs)
        self._db = database

    def __str__(self):
        return u'The Mongo "%s" database' % self._db

    def make_connection(self, **kwargs):
        '''
        override this method for change Mongo Connection class/object
        '''
        self._conn = MConn(**kwargs)

    @property
    def connection(self):
        return self._conn

    @property
    def db(self):
        #return self._conn[self._db]
        return getattr(self.connection, self._db)

    def __getattr__(self, item):
        if hasattr(self.db, item):
            return getattr(self.db, item)
        raise AttributeError(u'The Mongo Database object hasn`t "%s" attribute'\
                             % item)


# short alias
MDB = MongoDatabase