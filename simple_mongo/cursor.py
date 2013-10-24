#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


from simple_mongo import MDB


__all__ = ['MongoCursor', 'MCur']


class MongoCursor(MDB):
    _cursor = None

    def __init__(self, cursor, **kwargs):
        if cursor is None:
            raise AttributeError(u'The cursor attribute does not be a None')
        self._cursor = cursor
        super(MongoCursor, self).__init__(cursor.collection.database, **kwargs)

    def __getitem__(self, item):
        return self._cursor[item]


# short alias
MCur = MongoCursor