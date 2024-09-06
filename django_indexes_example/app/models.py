from django.db import models


class Book(models.Model):
    title = models.CharField(
        max_length=200, db_index=True
    )  # Django createes a Index on title
    author = models.CharField(max_length=100)
    publication_date = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=["author", "publication_date"])
        ]  # Composite index of book - author and publication_date fields

    def __str__(self):
        return self.title


"""
Explanation:
db_index=True on the title field creates a single-column index.
The Meta.indexes creates a composite index on both author and publication_year for optimizing queries that involve these two fields.

"""
