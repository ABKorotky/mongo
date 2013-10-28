#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from simple_mongo import MDB, MongoException
from simple_mongo.document import MDoc


class MCurException(MongoException):

    def __init__(self, **kwargs):
        number = kwargs.pop('number', 30)
        msg = kwargs.pop('msg', 'The basic Mongo Cursor Exception')
        super(MCurException, self).__init__(number=number, msg=msg)


class MCurNotInitializedException(MCurException):

    def __init__(self, _id):
        super(MCurException, self).__init__(number=31,
            msg='The Mongo Cursor does not initialized' % _id)


__all__ = ['MongoCursor', 'MCur']


class MongoCursor(MDB):
    _cursor = None

    def __init__(self, cursor, **kwargs):
        if cursor is None:
            raise AttributeError(u'The cursor attribute does not be a None')
        self._cursor = cursor
        super(MongoCursor, self).__init__(cursor.collection.database, **kwargs)

    def get_document_class(self):
        return MDoc

    def __getitem__(self, item):
        doc = self._cursor[item]
        return self.get_document_class()(doc=doc, collection=self._cursor.collection)

    def __getattr__(self, item):
        if hasattr(self._doc, item):
            return getattr(self._doc, item)
        raise AttributeError(u'The Mongo Cursor has not "%s" attribute' % item)


# short alias
MCur = MongoCursor