# I use here orm but in case of performance issue it is better to use sqlalchemy core


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, func, LargeBinary, VARBINARY, Integer, BINARY, VARCHAR, Enum, Float

# we should move this enum to different file, we will no longer depends on witai api
from witai import Value

Base = declarative_base()


class Url(Base):
    SALT_SIZE = 16
    __tablename__ = 'urls'
    created = Column(DateTime, nullable=False, server_default=func.now())
    salt = Column(BINARY(SALT_SIZE))

    # should have lenght of hash
    hash_of_url = Column(VARBINARY(512), nullable=False, primary_key=True)

    url = Column(VARCHAR(512), nullable=False, primary_key=True)

    analysis = Column(Enum(Value), nullable=False)
    confidence = Column(Float, nullable=False)


# maybe we need to add fk from urls in words?
class Word(Base):
    __tablename__ = 'words'
    created = Column(DateTime, nullable=False, server_default=func.now())
    last_modified = Column(DateTime, nullable=False, server_default=func.now(), server_onupdate=func.now())

    # should have lenght of hash
    word = Column(VARBINARY(512), primary_key=True)
    encrypted_word = Column(LargeBinary, nullable=False)
    occurrences = Column(Integer, nullable=False)
