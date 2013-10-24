# -*- coding: utf-8 -*-
__author__ = 'aleksandr'


from simple_mongo import MDB
from simple_mongo.collection import MC
from simple_mongo.document import MDoc
from simple_mongo.cursor import MCur


coll_1 = MC('simple_mongo', 'collection_1')
print len(coll_1)

doc = {
    'field_1': "12345",
    'field_2': "67890"
}

doc_1 = coll_1.create_doc(doc)
print doc_1
for k, v in doc_1.items():
    print "doc[%s] = %s" % (k, v)
