__author__ = 'root'

import random
from les_2 import get_db


def get_collection(dbh, name):
    return dbh[name]


def insert_doc(collection, **kwargs):
    collection.insert(kwargs if kwargs else {}, safe=True)


def main():
    dbh = get_db('lessons')
    age = range(20, 51)
    pets = ('dog', 'cat', 'fish', 'bird')
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
        insert_doc(get_collection(dbh, 'users'), **user)
        print "User %d inserted sussefully" % i


if __name__ == '__main__':
    main()