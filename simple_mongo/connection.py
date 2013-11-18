#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import exceptions


class BaseConnection(object):

    '''
    The basic connection class.
    It very simple class. Every time return new connection instance.
    '''

    def __new__(cls, **kwargs):
        return cls._make_connection(**kwargs)

    @staticmethod
    def _make_connection(**kwargs):
        try:
            return MongoClient(**kwargs)
        except ConnectionFailure:
            raise exceptions.MongoException(err_num=exceptions.CONNECTION_ERROR)


class SingleConnection(BaseConnection):

    '''
    This connection class realize 'PseudoSingleton' pattern.

    If we pass:
        conn_obj = Connection()
    we get a really Singleton.

    But if we pass:
        conn_obj = Connection(new_connection=True)
    we get a new different mongo connection class instance.
    '''

    _conn = None

    def __new__(cls, **kwargs):
        if kwargs.pop('new_connection', False):
            return cls._make_connection(**kwargs)
        else:
            if cls._conn is None:
                cls._conn = cls._make_connection(**kwargs)
            return cls._conn


class SetConnection(BaseConnection):

    '''
    This class create and store some connections and every time returned once of it.

    How to use:
        # create and return new connection class. Also store it inside class
    conn = SetConnection(conn_number=3, **conn_params)
        # create, store and return new connection class
    conn2 = SetConnection(**conn_params)
    conn3 = SetConnection(**conn_params)
        # Further, if we try create new connection instance we get one of list created earlier
    conn4 = SetConnection(**conn_params) # it`s instance will be equal the conn
    conn5 = SetConnection(**conn_params) # it`s instance will be equal the conn2
    ...
    So, if we one time create SetConnection instance, then we may create many connections
    and don`t fear problems with many counts of connections to database.

    By default SetConnection() will be create two connection as opposed to SingleConnection()
    '''

    _conn_list = []
    _conn_number = 2
    _current = 0

    def __new__(cls, **kwargs):
        cls._conn_number = kwargs.pop('conn_number', 2)
        curr = len(cls._conn_list)
        if curr < cls._conn_number:
            new_conn = cls._make_connection(**kwargs)
            cls._conn_list.append(new_conn)
            return new_conn
        else:
            conn = cls._conn_list[cls._current]
            cls._current += 1
            if cls._current == curr:
                cls._current = 0
            return conn


DefaultConnection = SingleConnection