from django.urls import path
from . import views

urlpatterns = [
    path("bulk-input/", views.bulk_input, name="bulk_input"),
    path("query-books/", views.query_books, name="query_books"),
    path("author-book-count/", views.author_book_count, name="author_book_count"),
]
