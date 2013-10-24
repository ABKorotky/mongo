__author__ = 'root'

import random
from pymongo import DESCENDING, ASCENDING
from les_2 import get_db
from les_3 import get_collection


def main():
    dbh = get_db('lessons')
    coll = get_collection(dbh, 'users')
    #coll.update(
    #    {'firstname': 'John'},
    #    {'$set': {'email': "email@site.com"}},
    #    safe=True, multi=True
    #)
    coll.update(
        {'firstname': 'Adam'},
        {'$set': {'sub_doc': {'property': random.choice([1,2,3,4,5])}}},
        multi=True, safe=True
    )

if __name__ == '__main__':
    main()