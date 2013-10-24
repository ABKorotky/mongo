# -*- coding: utf-8 -*-
__author__ = 'aleksandr'


from simple_mongo import MDB
from simple_mongo.collection import MC
from simple_mongo.document import MDoc
from simple_mongo.cursor import MCur


coll_1 = MC('simple_mongo', 'collection_1')
print len(coll_1)

cur_1 = coll_1.find()
for doc in cur_1:
    print "doc = %s" % doc
    for k, v in doc.items():
        print 'doc[%s] = %s' % (k, v)
