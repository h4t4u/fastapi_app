'''Pydantic models for data validation and serialization.'''

###  NOTICE: here I disable "too-few-public-methods" for pylint since
###  the model classes don't need additional methods.
###  There are too many of them to pass 7.5 mark otherwise.

from pydantic import BaseModel


class AuthorBase(BaseModel): # pylint: disable=too-few-public-methods
    '''Author base'''
    name: str


class AuthorCreate(AuthorBase): # pylint: disable=too-few-public-methods
    '''Author create'''


class Author(AuthorBase): # pylint: disable=too-few-public-methods
    '''Author class'''
    id: int

    class Config: # pylint: disable=too-few-public-methods
        '''Config'''
        orm_mode = True


class BookBase(BaseModel): # pylint: disable=too-few-public-methods
    '''Book base'''
    title: str
    year: int
    author_id: int


class BookCreate(BookBase): # pylint: disable=too-few-public-methods
    '''Book create'''


class Book(BookBase): # pylint: disable=too-few-public-methods
    '''Book class'''
    id: int

    class Config: # pylint: disable=too-few-public-methods
        '''Config'''
        orm_mode = True


class ReviewBase(BaseModel): # pylint: disable=too-few-public-methods
    '''Review base'''
    rating: int
    text: str
    book_id: int


class ReviewCreate(ReviewBase): # pylint: disable=too-few-public-methods
    '''Review create'''


class Review(ReviewBase): # pylint: disable=too-few-public-methods
    '''Review class'''
    id: int
    user_id: int

    class Config: # pylint: disable=too-few-public-methods
        '''Config'''
        orm_mode = True


class UserCreate(BaseModel): # pylint: disable=too-few-public-methods
    '''User create'''
    username: str
    password: str


class User(BaseModel): # pylint: disable=too-few-public-methods
    '''User class'''
    id: int
    username: str

    class Config: # pylint: disable=too-few-public-methods
        '''Config'''
        orm_mode = True
