# I use here orm but in case of performance issue it is better to use sqlalchemy core


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func, LargeBinary, VARBINARY, Integer

Base = declarative_base()


class Word(Base):
    __tablename__ = 'words'
    created = Column(DateTime, nullable=False, server_default=func.now())
    last_modified = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())

    # should have lenght of hash
    word = Column(VARBINARY(512), primary_key=True)

    encrypted_word = Column(LargeBinary, nullable=False)

    occurrences = Column(Integer, nullable=False)
