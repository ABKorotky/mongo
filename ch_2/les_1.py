__author__ = 'aleksandr'


from pymongo import Connection
from pymongo.errors import ConnectionFailure


def make_conn():
    try:
        conn = Connection(host='localhost', port=27017)
        print "Connected successfully"
        print conn.__dict__
        return conn
    except ConnectionFailure, e:
        print "error: %s" % e
        return None


if __name__ == "__main__":
    make_conn()