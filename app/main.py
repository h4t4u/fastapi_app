'''Main FastAPI app setup and routing.'''

from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app import crud, models, schemas
from app.database import engine, get_database
from app.auth import authenticate_user, create_access_token, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, database: Session = Depends(get_database)):
    '''
    Register method,

        :param database: Database session.
        :param user: User create scheme.
        :return: The user.
    '''
    return crud.create_user(database, user)


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(),\
             database: Session = Depends(get_database)):
    '''
    Login method,

        :param database: Database session.
        :param form_data: Form data.
        :return: The token.
    '''
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@app.get("/books", response_model=list[schemas.Book])
def read_books(database: Session = Depends(get_database)):
    '''
    Get books,

        :param database: Database session.
        :return: The books.
    '''
    return crud.get_books(database)


@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, database: Session = Depends(get_database)):
    '''
    Register method,

        :param database: Database session.
        :param book: Book create scheme.
        :return: The book.
    '''
    return crud.create_book(database, book)


@app.get("/books/{book_id}/rating")
def book_rating(book_id: int, database: Session = Depends(get_database)):
    '''
    Get book rating,

        :param database: Database session.
        :param book_id: Book id.
        :return: The rating.
    '''
    return crud.get_book_rating(database, book_id)


@app.post("/reviews", response_model=schemas.Review)
def create_review(
    review: schemas.ReviewCreate,
    database: Session = Depends(get_database),
    current_user: schemas.User = Depends(get_current_user)
):
    '''
    Create review,

        :param database: Database session.
        :param current_uuser: Current user.
        :param review: Review create scheme.
        :return: The review.
    '''
    return crud.create_review(database, review, current_user.id)

@app.get("/authors", response_model=list[schemas.Author])
def get_authors(database: Session = Depends(get_database)):
    '''
    Get authors,

        :param database: Database session.
        :return: The authors.
    '''
    return crud.get_authors(database)

@app.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, database: Session = Depends(get_database)):
    '''
    Create author,

        :param database: Database session.
        :param author: Author scheme.
        :return: The books.
    '''
    return crud.create_author(database, author)


@app.delete("/users/{username}")
def delete_user(username: str, database: Session = Depends(get_database)):
    '''
    Delete user,

        :param database: Database session.
        :param username: User name.
        :return: The deleted user.
    '''
    try:
        deleted_user = crud.delete_user_by_username(database=database, username=username)
        return {"message": f"User {deleted_user.username} deleted successfully."}
    except NoResultFound as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/books/{book_id}")
def delete_book(book_id: int, database: Session = Depends(get_database)):
    '''
    Delete book,

        :param database: Database session.
        :param book_id: Book id.
        :return: The deleted user.
    '''
    try:
        deleted_book = crud.delete_book(database=database, book_id=book_id)
        return {"message": f"Book '{deleted_book.title}' deleted successfully."}
    except NoResultFound as error:
        raise HTTPException(status_code=404, detail=str(e))