__author__ = 'aleksandr'

from ch_2.les_2 import get_db
from ch_2.les_3 import get_collection


def main():
    usr = 'Gvido van Rossum'
    user_doc = {
        'username': usr,
        'emails': []
    }
    coll = get_collection(get_db('lessons'), 'users_ext')
    if not coll.find_one({'username': usr}):
        coll.insert(user_doc, safe=True)
    user = coll.find_one({'username': usr})
    user.emails.append({'email': 'username@email1.com'})




if __name__ == '__main__':
    main()