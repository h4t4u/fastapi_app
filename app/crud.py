'''CRUD operations for interacting with the database.'''

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from passlib.hash import bcrypt
from app import models, schemas


def get_user_by_username(database: Session, username: str):
    '''
    Get user by username,

        :param database: Database session.
        :param username: User name.
        :return: The user.
    '''

    return database.query(models.User).filter(models.User.username == username).first()


def create_user(database: Session, user: schemas.UserCreate):
    '''
    Create user,

        :param database: Database session.
        :param user: User to be created.
        :return: The user.
    '''

    hashed_password = bcrypt.hash(user.password)
    database_user = models.User(username=user.username, hashed_password=hashed_password)
    database.add(database_user)
    database.commit()
    database.refresh(database_user)
    return database_user


def create_author(database: Session, author: schemas.AuthorCreate):
    '''
    Create author,

        :param database: Database session.
        :param author: Author to be created.
        :return: The author.
    '''

    database_author = models.Author(**author.dict())
    database.add(database_author)
    database.commit()
    database.refresh(database_author)
    return database_author


def get_authors(database: Session):
    '''
    Get all authors,

        :param database: Database session.
        :return: The authors.
    '''

    return database.query(models.Author).all()


def create_book(database: Session, book: schemas.BookCreate):
    '''
    Create book,

        :param database: Database session.
        :param book: Book to be created.
        :return: The book.
    '''

    database_book = models.Book(**book.dict())
    database.add(database_book)
    database.commit()
    database.refresh(database_book)
    return database_book


def get_books(database: Session):
    '''
    Get all books,

        :param database: Database session.
        :return: The books.
    '''

    return database.query(models.Book).all()


def get_book_rating(database: Session, book_id: int):
    '''
    Get book rating,

        :param database: Database session.
        :param book_id: Book id to be rated.
        :return: The book rating.
    '''

    book = database.query(models.Book).filter(models.Book.id == book_id).first()
    if not book or not book.reviews:
        return {"rating": None}
    avg_rating = sum([r.rating for r in book.reviews]) / len(book.reviews)
    return {"rating": avg_rating}


def create_review(database: Session, review: schemas.ReviewCreate, user_id: int):
    '''
    Create review,

        :param database: Database session.
        :param review: Review to be created.
        :return: The review.
    '''

    database_review = models.Review(**review.dict(), user_id=user_id)
    database.add(database_review)
    database.commit()
    database.refresh(database_review)
    return database_review


def delete_user_by_username(database: Session, username: str):
    '''
    Delete user,

        :param database: Database session.
        :param username: Username to be deleted.
        :return: The deleted user.
    '''
    database_user = database.query(models.User).filter(models.User.username == username).first()

    if database_user:
        database.delete(database_user)
        database.commit()
        return database_user
    raise NoResultFound(f"User with name '{username}' not found")

def delete_book(database: Session, book_id: int):
    '''
    Delete book,

        :param database: Database session.
        :param book_id: Book to be deleted.
        :return: The deleted book.
    '''
    database_book = database.query(models.Book).filter(models.Book.id == book_id).first()

    if database_book:
        database.delete(database_book)
        database.commit()
        return database_book
    raise NoResultFound(f"Book with id '{book_id}' not found")
