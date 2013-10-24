__author__ = 'aleksandr'

from ch_2.les_1 import make_conn


def get_db(db_name):
    conn = make_conn()
    if conn:
        return conn[db_name]
    return None


def main():
    dbh = get_db('test')
    print "database handler created"
    print dbh.__dict__


if __name__ == "__main__":
    main()