from django.db import models


class Author(models.Model):
    full_name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    isbn = models.CharField(max_length=20, blank=True)
    isbn13 = models.CharField(max_length=20, blank=True)
    num_pages = models.PositiveSmallIntegerField(null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)

    authors = models.ManyToManyField(
        'api_books.Author',
        related_name='books',
    )
