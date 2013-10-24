# -*- coding: utf-8 -*-
__author__ = 'aleksandr'


from my_mongo import MConn, MDB, MC


def test_conn():
    print "----- test connection objects -----"
    c1 = MConn()
    c2 = MConn()
    c3 = MConn(new_connection=True)
    print "id(c1) = %s" % id(c1)
    print "id(c2) = %s" % id(c2)
    print "id(c3) = %s" % id(c3)


def test_db():
    print "----- test database objects -----"
    db1 = MDB('tests')
    db2 = MDB('lessons')
    db3 = MDB('utils', new_connection=True)
    print "db1.__dict__ = %s; id(db1._conn) = %s" % (db1.__dict__, id(db1._conn))
    print "db2.__dict__ = %s; id(db2._conn) = %s" % (db2.__dict__, id(db2._conn))
    print "db3.__dict__ = %s; id(db3._conn) = %s" % (db3.__dict__, id(db3._conn))


def test_collection():
    print "----- test collection object -----"
    mc1 = MC('test', 'collection_1')
    mc2 = MC('test', 'collection_2')



def main():
    print "It`s main function"
    test_conn()
    print "\n\n"
    test_db()
    print "\n\n"
    test_collection()


if __name__ == "__main__":
    main()