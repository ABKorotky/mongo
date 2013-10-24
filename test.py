# -*- coding: utf-8 -*-
__author__ = 'aleksandr'


from simple_mongo.collection import MC
from simple_mongo.document import MDoc
from simple_mongo.cursor import MCur


coll_1 = MC('simple_mongo', 'collection_1')
print len(coll_1)
print coll_1.db.collection_names()
#cur_1 = coll_1.find()
#for doc in cur_1:
#    print "doc = %s" % doc
#    for k, v in doc.items():
#        print 'doc[%s] = %s' % (k, v)

print coll_1.find_doc(query={'firstname': "Adam", 'lastname': "Doe"})
print coll_1.find_doc(_id='526966bb25e7064f73b54451')

d1 = MDoc()
print d1
