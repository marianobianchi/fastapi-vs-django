from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Table
from sqlalchemy.orm import relationship

from .database import Base


association_table = Table('BookAuthors', Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('book_id', Integer, ForeignKey('books.id'))
)


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String)
    isbn13 = Column(String)
    num_pages = Column(Integer)
    publication_date = Column(Date)

    authors = relationship(
        'Author',
        secondary=association_table,
        back_populates='books')


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)

    books = relationship(
        'Book',
        secondary=association_table,
        back_populates='authors')
