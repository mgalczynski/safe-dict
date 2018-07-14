from collections import namedtuple
from operator import itemgetter
from hashlib import sha3_512
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

import rsa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.concurrent import run_on_executor

from db.models import Word, Base

DecryptedWord = namedtuple('DecryptedWord', ('word', 'occurrences', 'created', 'last_modified'))


class Repository:
    SALT_SIZE = 32

    # we have same salt for every word that has one advantage: we can look without knowledge of private key
    # and one disadvantage: it easier to have collision
    def __init__(self, public_key, db_url, salt, private_key=None):
        if len(salt) != self.SALT_SIZE:
            raise RuntimeError('Not correct salt size')
        self.salt = salt
        self.executor = ThreadPoolExecutor(10)
        self.public_key = public_key
        self.private_key = private_key
        engine = create_engine(db_url)
        self.Session = sessionmaker(bind=engine)
        # for developing only, later for production should be removed
        Base.metadata.create_all(engine)

    @run_on_executor
    def save(self, url, results):
        # we need to do something with sessions, we should be sure that is one session per request (some di)
        session = self.Session()
        try:
            for word, occurrences in sorted(results.items(), key=itemgetter(1), reverse=True):
                hash_of_word = sha3_512(self.salt + word.encode()).digest()
                encrypted_word = rsa.encrypt(word.encode(), self.public_key)
                # last_modified is needed when rest of property is same as in db
                session.merge(Word(word=hash_of_word, encrypted_word=encrypted_word, occurrences=occurrences,
                                   last_modified=datetime.utcnow()))

            session.commit()
        except:
            session.rollback()
            raise

    @run_on_executor
    def get_all_words(self):
        if self.private_key is None:
            raise RuntimeError('To execute this method private key is needed')
        # we need to do something with sessions, we should be sure that is one session per request (some di)
        session = self.Session()

        try:
            return [DecryptedWord(rsa.decrypt(w.encrypted_word, self.private_key).decode(),
                                  w.occurrences,
                                  w.created,
                                  w.last_modified)
                    for w in session.query(Word).all()]
        except rsa.DecryptionError:
            return 500, 'Internal error'
        except UnicodeDecodeError:
            return 500, 'Internal error'
