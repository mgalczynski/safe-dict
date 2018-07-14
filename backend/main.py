from secrets import token_bytes
from hashlib import sha3_512

import rsa
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from scrapper import Scrapper
from db.models import Page, Word, Base

engine = create_engine('mysql+mysqlconnector://root:password@localhost/dict')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)



if __name__ == '__main__':
    session = Session()
    url = 'https://en.wikipedia.org/wiki/Poland'

    with open('public.pem', 'rb') as public:
        public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public.read())


    try:
        page = Page(url=url)
        session.add(page)
        session.flush()
        results = Scrapper.scape(url)
        for word, frequency in results.items():
            salt = token_bytes(16)
            hash_of_word = sha3_512(url.encode() + salt + word.encode()).digest()
            encrypted_word = rsa.encrypt(word.encode(), public_key)
            session.add(
                Word(page_id=page.id, salt=salt, word=hash_of_word, encrypted_word=encrypted_word, raw_word=word,
                     count=frequency))

        session.commit()
    except:
        session.rollback()
        raise
