# -*- coding: utf-8 -*-
__author__ = 'aleksandr'

import random
from simple_mongo.collection import MC
from simple_mongo.document import MDoc
from simple_mongo.cursor import MCur


coll_1 = MC('simple_mongo', 'collection_1')

d1 = coll_1.find_doc(query={'firstname': "Bill", 'lastname': "Doe"})
print "d1 before change: %s" % d1
print "d1._xid = %s" % d1._xid

d1['age'] = random.choice(range(20, 51))
if not d1.has_key('pets'):
    d1['pets'] = []
else:
    d1['pets'].append('dog')
print "d1._map = %s" % d1._map
print "d1 after change: %s" % d1

print "save result: %s" % d1.save()
d1.refresh()
print "d1 after refresh: %s" % d1