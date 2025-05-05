'''SQLAlchemy models for database entities.'''

###NOTICE: here I disable "too-few-public-methods" for pylint since the model classes don't need additional methods. There are too many of them to pass otherwise.

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class User(Base): # pylint: disable=too-few-public-methods
    '''User class'''

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    reviews = relationship("Review", back_populates="user")


class Author(Base): # pylint: disable=too-few-public-methods
    '''Author class'''

    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    books = relationship("Book", back_populates="author")


class Book(Base): # pylint: disable=too-few-public-methods
    '''Book class'''

    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    year = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))

    author = relationship("Author", back_populates="books")
    reviews = relationship("Review", back_populates="book")


class Review(Base): # pylint: disable=too-few-public-methods
    '''Review class'''

    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    text = Column(String)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
