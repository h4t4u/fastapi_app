from app.test_main import test_create_author, test_get_books, test_get_book_rating
from app.test_main import test_create_book, test_create_review, token

tk = token()
test_create_author()
test_create_book(tk)
test_create_review(tk)
test_get_books()
test_get_book_rating()
test_delete_book()