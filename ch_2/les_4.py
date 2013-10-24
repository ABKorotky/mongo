__author__ = 'root'

from pymongo import DESCENDING, ASCENDING
from les_2 import get_db
from les_3 import get_collection


def find_all_by_dict(coll, d):
    return coll.find(d)


def find_all_by_key_val(coll, key, val):
    return coll.find({key: val})


def find_all_Johns(coll):
    return find_all_by_key_val(coll, 'firstname', 'John')


def main():
    dbh = get_db('lessons')
    coll = get_collection(dbh, 'users')
    #seq = find_all_by_dict(coll, {'pets': {'$exists': True, '$size': 2}, '$or': [{'pets': {'$all': ['cat']}}, {'pets': {'$all': ['dog']}}]})
    #seq = find_all_by_dict(coll, {'$or': [{'firstname': 'John'}, {'lastname': 'Doe'}], 'pets': {'$exists': True}})
    #seq = coll.find()
    seq = coll.find({'sub_doc.property': 2})
    for user in seq:
        print user
    print "=" * 100
    print "Total documents: %d" % seq.count()

if __name__ == '__main__':
    main()