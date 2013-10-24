# -*- coding: utf-8 -*-
__author__ = 'aleksandr'


from pymongo import Connection
from pymongo.errors import ConnectionFailure


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


class MongoCollection(MongoDatabase):

    _collection = None

    def __init__(self, database, collection, **kwargs):
        super(MongoCollection, self).__init__(database, **kwargs)
        self._collection = collection

    def __str__(self):
        return u'The Mongo "%s.%s" collection' % (self._db, self._collection)

    @property
    def collection(self):
        if self.db is not None:
            return getattr(self.db, self._collection)
        else:
            return None

    def __len__(self):
        if self.collection is not None:
            return self.collection.find({}).count()
        else:
            return 0


# short alias
MC = MongoCollection


class MongoDocument(MongoDatabase):

    _collection = None
    _doc = None
    _xid = None

    def __init__(self, database, collection, xid, **kwargs):
        super(MongoDocument, self).__init__(database, **kwargs)
        self._collection = collection
        #TODO - insert initialisation document functionality

    def __str__(self):
        if self._xid:
            return u'The Mongo <%s> document from "%s.%s" collection' % (self._xid, self._db, self._collection)
        else:
            return u'The not initialized Mongo document from "%s.%s" collection' % (self._db, self._collection)


class MongoCursor(MongoDatabase):

    _