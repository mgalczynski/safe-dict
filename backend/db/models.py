# I use here orm but in case of performance issue it is better to use sqlalchemy core


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, String, DateTime, func, BINARY, LargeBinary, VARBINARY, Integer

Base = declarative_base()


class Page(Base):
    __tablename__ = 'pages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, nullable=False, server_default=func.now())
    url = Column(String(100))


class Word(Base):
    __tablename__ = 'words'
    page_id = Column(Integer, ForeignKey('pages.id'), nullable=False)

    salt = Column(BINARY(16), nullable=False)

    # should have lenght of hash
    word = Column(VARBINARY(512), primary_key=True)

    encrypted_word = Column(LargeBinary, nullable=False)

    occurrences = Column(Integer, nullable=False)
