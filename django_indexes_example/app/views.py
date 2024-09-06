from django.shortcuts import render, redirect
from .models import Book
from django.db.models import Count
import json
from datetime import datetime


def bulk_input(request):
    if request.method == "POST":
        json_input = request.POST.get("json_input")

        try:
            # Parse the JSON data
            books_data = json.loads(json_input)
            books_to_create = []

            # Loop through each book and create a Book instance
            for book_data in books_data:
                title = book_data.get("title")
                author = book_data.get("author")
                publication_year = book_data.get("publication_year")

                if title and author and publication_year:
                    # Convert year to a full date (e.g., January 1st of that year)
                    publication_date = datetime(
                        year=int(publication_year), month=1, day=1
                    ).date()

                    books_to_create.append(
                        Book(
                            title=title,
                            author=author,
                            publication_date=publication_date,
                        )
                    )
            # Bulk create the book entries in the database
            if books_to_create:
                Book.objects.bulk_create(books_to_create)
                message = f"Successfully added {len(books_to_create)} books."
            else:
                message = "No valid data to add."

        except json.JSONDecodeError:
            message = "Invalid JSON format."

        return render(request, "books/bulk_input.html", {"message": message})

    return render(request, "books/bulk_input.html")


# View to query books by author and publication year (example of indexing usage)
def query_books(request):
    # Example: Find all books by George Orwell published in 1949
    books_by_orwell = Book.objects.filter(
        author="J.R.R. Tolkien", publication_date__year=1937
    )

    print(books_by_orwell)

    return render(request, "books/query_result.html", {"books": books_by_orwell})


# View to perform a join-like operation (though Django uses ORM to do this efficiently)
def author_book_count(request):
    # Example: Get each author and count of their books
    author_counts = (
        Book.objects.values("author")
        .annotate(book_count=Count("id"))
        .order_by("-book_count")
    )

    return render(
        request, "books/author_book_count.html", {"author_counts": author_counts}
    )
