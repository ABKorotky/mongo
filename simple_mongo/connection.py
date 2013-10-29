#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from pymongo import Connection, MongoClient
from pymongo.errors import ConnectionFailure
import exceptions


__all__ = ['MongoConnection', 'MConn', 'MongoClientConnection', 'MClientConn']


class BaseConnection(object):

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
        if kwargs.pop('new_connection', False):
            return cls._make_connection(**kwargs)
        else:
            if cls._conn is None:
                cls._conn = cls._make_connection(**kwargs)
            return cls._conn

    @staticmethod
    def _make_connection(**kwargs):
        raise NotImplementedError(u'The method "_make_connection" does not \
        realise. Please override this method in any/every descendant class.')


class MongoClientConnection(BaseConnection):

    @staticmethod
    def _make_connection(**kwargs):
        try:
            return MongoClient(**kwargs)
        except ConnectionFailure:
            MongoClientConnection.logging()
            raise exceptions.MongoException(err_num=exceptions.CONNECTION_ERROR)

    @staticmethod
    def logging():
        '''
        override this method for adding logging functionality
        '''
        pass


# short alias
MClientConn = MongoClientConnection


class MongoConnection(BaseConnection):

    @staticmethod
    def _make_connection(**kwargs):
        try:
            return Connection(**kwargs)
        except ConnectionFailure:
            MongoConnection.logging()
            raise exceptions.MongoException(err_num=exceptions.CONNECTION_ERROR)

    @staticmethod
    def logging():
        '''
        override this method for adding logging functionality
        '''
        pass


# short alias
MConn = MongoConnection