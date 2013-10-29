#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from simple_mongo.connection import MongoClientConnection
from simple_mongo.collection import MongoCollection


class MyConnection(MongoClientConnection):

    '''
    for example we inherit from MongoClientConnection.
    There are we can override a _make_connection staticmethod or override
    logging staticmethod od add any amount of additional methods...

    Warning!!! It is important!
    the method __new__ must return a mongo Connection instance.
    '''

    pass


class MyCollection(MongoCollection):

    def use_connection(self, **kwargs):
        '''
        this method will be call in __init__ method.
        '''
        self._conn = MyConnection(*kwargs)