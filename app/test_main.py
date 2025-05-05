'''Test module for the app.'''

import pytest
from fastapi.testclient import TestClient
from app.main import app
from random_username.generate import generate_username
from sqlalchemy.exc import NoResultFound

client = TestClient(app)

VERBOSE = True

@pytest.fixture(scope="module")
def token():
    '''Test token work'''

    username = generate_username(1)[0]
    response = client.post("/register", json={"username": username, "password": "testpass"})
    assert response.status_code in (200, 400)

    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]

    if VERBOSE:
        print("Token work checked")

def test_create_author():
    '''Test create author'''
    name = "Leo Tolstoy"
    response = client.post("/authors", json={"name": name})
    assert response.status_code == 200
    assert response.json()["name"] == "Leo Tolstoy"

    if VERBOSE:
        print(f"Author {name} created")


def test_create_book(token):
    '''Test create book'''
    authors = client.get("/authors").json()
    author_id = authors[0]["id"]
    title = "War and Peace"
    year = 1869

    response = client.post(
        "/books",
        json={"title": title, "year": year, "author_id": author_id}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "War and Peace"

    if VERBOSE:
        print(f"Book {title} of year {year} created.")

def test_create_review(token):
    '''Test create review'''
    books = client.get("/books").json()
    book_id = books[0]["id"]

    response = client.post(
        "/reviews",
        json={"rating": 5, "text": "Masterpiece!", "book_id": book_id},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["rating"] == 5

    if VERBOSE:
        print(f"Review on book {book_id} with mark 5 created.")

def test_get_books():
    '''Test get books'''
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    if VERBOSE:
        print("Got books.")

def test_get_book_rating():
    '''Test get book rating'''
    books = client.get("/books").json()
    book_id = books[0]["id"]
    response = client.get(f"/books/{book_id}/rating")
    assert response.status_code == 200
    assert "rating" in response.json()

    if VERBOSE:
        rating = response.json()["rating"]
        print(f"Got rating of book {book_id}. It is {rating}.")


def test_delete_book():
    '''Test delete book'''
    books = client.get("/books").json()
    book_id = books[0]["id"]

    response = client.delete(f"/books/{book_id}")
    assert response.status_code == 200

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 405
