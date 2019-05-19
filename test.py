import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Sequence, column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, selectinload

url = 'postgresql+psycopg2://shumnyj:111@localhost:5432/testpost'

engine = create_engine(url, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,  primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    nickname = Column(String(50))

    addresses = relationship("Address", back_populates='user', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(name='%s', fullname='%s', nickname='%s')>" % (self.name, self.fullname, self.nickname)


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return "<Address(email_address='%s')>" % self.email_address


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
        return "<Author(fname='%s', sname='%s', exp='%d',  written='%d' publisher='%s')>" %\
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


# User.addresses = relationship("Address", order_by=Address.id, back_populates="user")

class YEET:
    x = 0


Base.metadata.create_all(engine)
session = Session()

"""ed_user = User(name='ed', fullname='Ed Jones', nickname='edsnickname')
session.add(ed_user)
session.commit()
our_user = session.query(User).filter_by(name='ed').first()
our_user.nickname = "nibba"
session.commit()"""

x = Book.col()[0]
print(type(Book.title))
print(x)
a = column(x[0])
p = session.query(Book).filter_by(author_fname='fname2').first()
cl = YEET()
name = 'wq'

print(getattr(p, 'title'))
print(setattr(p, 'title', 'oop'))
print(session.dirty)
"""p = session.query(Author).options(selectinload(Author.books_f)).filter_by(fname='fname2').one()
for x in p.books_f:
    print(x.title)"""

# session.add(ed_user)
# session.add_all([User(name='wendy', fullname='Wendy Williams', nickname='windy'),
#                  User(name='mary', fullname='Mary Contrary', nickname='mary'),
#                  User(name='fred', fullname='Fred Flintstone', nickname='freddy')])
# our_user = session.query(User).filter_by(name='ed').first()
# session.commit()

"""jack = User(name='jack', fullname='Jack Bean', nickname='gjffdd')
jack.addresses = [Address(email_address='jack@google.com'),Address(email_address='j25@yahoo.com')]
session.add(jack)
session.commit()

jack = session.query(User).options(selectinload(User.addresses)).filter_by(name='jack').one()
x = jack.addresses

del jack.addresses[1]

x = jack.addresses

session.delete()
x = session.query(User).filter_by(name='jack').count()
x = session.query(Address).filter(Address.email_address.in_(['jack@google.com', 'j25@yahoo.com'])).count()
session.commit()"""

"""for instance in session.query(Author).order_by(Author.exp):
    print(instance.fname, instance.sname)
for instance in session.query(Book).order_by(Book.pages):
    print(instance.title, instance.barcode, instance.pages)
for instance in session.query(Publisher):
    print(instance)"""
# for row in session.query(User, User.name).all():
#     print(row.User, row.name)


