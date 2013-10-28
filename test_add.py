#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Alexander Korotky'


import random
from simple_mongo.collection import MC


def main():
    age = range(20, 51)
    pets = ('dog', 'cat', 'fish', 'bird')
    mc = MC('simple_mongo', 'collection_1')
    if len(mc):
        mc.drop()
    for i in range(100):
        user = {
            'firstname': random.choice(('John', 'Adam', 'Bill', 'Bob')),
            'lastname': random.choice(('Smith', 'Rossum', 'Einstain', 'Doe')),
            'age': random.choice(age)
        }
        if random.choice((True, False)):
            pets_s = set()
            for j in range(random.choice((1, 2, 3))):
                pets_s.add(random.choice(pets))
            user.update(pets=list(pets_s))
        mc.create_doc(user)
        print "User %d inserted sussefully" % i



if __name__ == '__main__':
    main()