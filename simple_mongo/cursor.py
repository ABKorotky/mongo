#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from simple_mongo import MDB
from document import MDoc


__all__ = ['MongoCursor', 'MCur']


class MongoCursor(MDB):
    _cursor = None
    _collection = None

    def __init__(self, cursor, **kwargs):
        if cursor is None:
            raise AttributeError(u'The cursor attribute does not be a None')
        self._cursor = cursor
        self._collection = cursor.collection
        super(MongoCursor, self).__init__(cursor.collection.database, **kwargs)

    def get_document_class(self):
        return MDoc

    def __getitem__(self, item):
        doc = self._cursor[item]
        return self.get_document_class()(doc=doc, collection=self._collection)

    def __getattr__(self, item):
        if hasattr(self._cursor, item):
            return getattr(self._cursor, item)
        raise AttributeError(u'The "%s" instance has not "%s" attribute' %
                                 (self.__class__.__name__, item))


# short alias
MCur = MongoCursor