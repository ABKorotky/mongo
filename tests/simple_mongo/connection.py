#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'

import unittest
from simple_mongo.connection import BaseConnection, SingleConnection, SetConnection


class TestConnection(unittest.TestCase):

    def test_baseConnection(self):
        conn1 = BaseConnection()
        conn2 = BaseConnection()
        self.assertNotEqual(id(conn1), id(conn2))

    def test_singleConnection(self):
        conn1 = SingleConnection()
        conn2 = SingleConnection()
        conn3 = SingleConnection()
        conn4 = SingleConnection(new_connection=True)
        self.assertEqual(id(conn1), id(conn2))
        self.assertEqual(id(conn1), id(conn3))
        self.assertNotEqual(id(conn1), id(conn4))

    def test_setConnection2(self):
        pool = []
        pool.append(SetConnection())
        pool.append(SetConnection())
        for i in xrange(10):
            test_conn = SetConnection()
            self.assertIn(test_conn, pool)

    def test_setConnection4(self):
        pool = []
        pool.append(SetConnection(conn_number=4))
        pool.append(SetConnection())
        pool.append(SetConnection())
        pool.append(SetConnection())
        for i in xrange(20):
            test_conn = SetConnection()
            self.assertIn(test_conn, pool)


if __name__ == '__main__':
    unittest.main()