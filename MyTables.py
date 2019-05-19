from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publishers'

    pname = Column(String(64), primary_key=True)
    address = Column(String(100))
    publ = Column(Integer)
    director = Column(String(64))

    authors = relationship("Author", back_populates='pbs', cascade="all, delete, delete-orphan")
    books = relationship("Book", back_populates='pbs', cascade="all, delete, delete-orphan")

    @staticmethod
    def col():
        return ('pname', 'address', 'publ', 'director'), ('varchar(64)', 'varchar(100)', 'integer', 'varchar(64)')

    def __repr__(self):
        return "<Publisher(pname='%s', address='%s', publ='%d',  director='%s')>" %\
               (self.pname, self.address, self.publ, self.director)

    def __init__(self, record):
        if len(record) == 4:
            self.pname = record[0]
            self.address = record[1]
            self.publ = record[2]
            self.director = record[3]
        else:
            return None


class Author(Base):
    __tablename__ = 'authors'

    fname = Column(String(32), primary_key=True)
    sname = Column(String(32), primary_key=True)
    exp = Column(Integer)
    written = Column(Integer)
    publisher = Column(String(64), ForeignKey('publishers.pname'))

    pbs = relationship("Publisher", back_populates="authors")

    books_f = relationship("Book", back_populates='fname', foreign_keys="[Book.author_fname]", cascade="all, delete, delete-orphan")
    books_s = relationship("Book", back_populates='sname', foreign_keys="[Book.author_sname]", cascade="all, delete, delete-orphan")

    @staticmethod
    def col():
        return ('fname', 'sname', 'exp', 'written', 'publisher'), \
               ('varchar(32)', 'varchar(32)', 'integer', 'integer', 'varchar(64)')

    def __repr__(self):
        return "<Author(fname='%s', sname='%s', exp='%d', written='%d' publisher='%s')>" %\
               (self.fname, self.sname, self.exp, self.written, self.publisher)

    def __init__(self, record):
        if len(record) == 5:
            self.fname = record[0]
            self.sname = record[1]
            self.exp = record[2]
            self.written = record[3]
            self.publisher = record[4]
        else:
            return None


class Book(Base):
    __tablename__ = 'books'

    title = Column(String(64))
    pages = Column(Integer)
    barcode = Column(Integer, primary_key=True)
    printing = Column(Boolean)
    author_fname = Column(String(32), ForeignKey('authors.fname'))
    author_sname = Column(String(32), ForeignKey('authors.sname'))
    pub = Column(String(64), ForeignKey('publishers.pname'))

    fname = relationship("Author", back_populates="books_f", foreign_keys=[author_fname])
    sname = relationship("Author", back_populates="books_s", foreign_keys=[author_sname])
    pbs = relationship("Publisher", back_populates="books")

    @staticmethod
    def col():
        return ('title', 'pages', 'barcode', 'printing', 'author_fname', 'author_sname', 'pub'), \
               ('varchar(64)', 'integer', 'integer', 'boolean', 'varchar(32)', 'varchar(32)', 'varchar(64)')

    def __repr__(self):
        return "<Book(title='%s', pages='%d', barcode='%d', printing='%d')>" %\
               (self.title, self.pages, self.barcode, self.printing)

    def __init__(self, record):
        if len(record) == 7:
            self.title = record[0]
            self.pages = record[1]
            self.barcode = record[2]
            self.printing = record[3]
            self.author_fname = record[4]
            self.author_sname = record[5]
            self.pub = record[6]
        else:
            return None
