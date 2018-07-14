from collections import namedtuple
from secrets import token_bytes
from hashlib import sha3_512
from concurrent.futures import ThreadPoolExecutor

import rsa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tornado.concurrent import run_on_executor

from db.models import Page, Word, Base

DecryptedWord = namedtuple('DecryptedWord', ('word', 'occurrences'))


class Repository:
    def __init__(self, public_key, db_url, private_key=None):
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
            page = Page(url=url)
            session.add(page)
            session.flush()
            for word, occurrences in results.items():
                salt = token_bytes(16)
                hash_of_word = sha3_512(url.encode() + salt + word.encode()).digest()
                encrypted_word = rsa.encrypt(word.encode(), self.public_key)
                session.add(
                    Word(page_id=page.id, salt=salt, word=hash_of_word, encrypted_word=encrypted_word,
                         occurrences=occurrences))

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
            return [DecryptedWord(rsa.decrypt(w.encrypted_word, self.private_key).decode(), w.occurrences)
                    for w in session.query(Word).all()]
        except rsa.DecryptionError:
            return 500, 'Internal error'
        except UnicodeDecodeError:
            return 500, 'Internal error'
