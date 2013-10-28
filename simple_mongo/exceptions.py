#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


MONGO_ERROR = 1
CONNECTION_ERROR = 2

COLLECTION_ERROR = 10

CURSOR_ERROR = 20

DOCUMENT_ERROR = 30
COLLECTION_MISSING = 31
DOCUMENT_LOAD_ERROR = 32


_messages = {
    MONGO_ERROR: u'The basic Mondo Exception',
    CONNECTION_ERROR: u'Unable to create Mongo Connection. You have errors',

    COLLECTION_ERROR: u'The basic Mondo Collection Exception',

    CURSOR_ERROR: u'The basic Mongo Cursor Exception',

    DOCUMENT_ERROR: u'The basic Mongo Document Exception',
    COLLECTION_MISSING: u'The "collection" attribute does not defined',
    DOCUMENT_LOAD_ERROR: u'Unable to load document: \
                        the "_id" attribute does not defined',
}


class MongoException(Exception):

    def __init__(self, err_num=MONGO_ERROR):
        self.args = (err_num, _messages[err_num])