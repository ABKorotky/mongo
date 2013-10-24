__author__ = 'root'

from pymongo import DESCENDING, ASCENDING
from les_2 import get_db
from les_3 import get_collection


def main():
    dbh = get_db('lessons')
    coll = get_collection(dbh, 'users')
    #coll.remove(
    #    {'firstname': 'John'},
    #    safe=True,
    #)
    coll.remove(safe=True)

if __name__ == '__main__':
    main()