#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

import unittest
import pymongo.connection
from simple_mongo.connection import BaseConnection
from simple_mongo.database import Database
from simple_mongo.collection import Collection


SM_TEST_DB = 'simple_mongo_test_db'
SM_TEST_DB2 = 'simple_mongo_test_db2'
SM_TEST_COLLECTION = 'test_collection'


class DatabaseTest(unittest.TestCase):
    _conn = None

    @classmethod
    def setUpClass(cls):
        cls._conn = pymongo.connection.MongoClient()
        names = cls._conn.database_names()
        if SM_TEST_DB not in names:
            cls._conn[SM_TEST_DB].create_collection(SM_TEST_COLLECTION)
        if SM_TEST_DB2 not in names:
            cls._conn[SM_TEST_DB2].create_collection(SM_TEST_COLLECTION)

    @classmethod
    def tearDownClass(cls):
        names = cls._conn.database_names()
        if SM_TEST_DB in names:
            cls._conn.drop_database(SM_TEST_DB)
        if SM_TEST_DB2 in names:
            cls._conn.drop_database(SM_TEST_DB2)

    def test_database(self):
        self.assertIsNotNone(Database(SM_TEST_DB))

    def test_get_collection(self):

        class TestCollection(Collection):
            pass

        test_db = Database(SM_TEST_DB,
            collection_map={SM_TEST_COLLECTION: TestCollection})
        test_coll = test_db.get_collection(SM_TEST_COLLECTION)
        self.assertIsInstance(test_coll, TestCollection)

    def test_default_connection(self):
        '''
        WARNING!!! The default connection class is SingleConnection class
        '''
        db1 = Database(SM_TEST_DB)
        db2 = Database(SM_TEST_DB2)
        self.assertEqual(id(db1.connection), id(db2.connection))

    def test_custom_connection(self):
        db1 = Database(SM_TEST_DB, connection=BaseConnection)
        db2 = Database(SM_TEST_DB2, connection=BaseConnection)
        self.assertNotEqual(id(db1.connection), id(db2.connection))


if __name__ == '__main__':
    unittest.main()