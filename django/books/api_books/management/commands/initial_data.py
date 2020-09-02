from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from .book_csv_reader import get_books
from api_books.models import Author, Book


class Command(BaseCommand):
    help = 'Creates initial data'

    def handle(self, *args, **options):
        books = get_books()
        for idx, book in enumerate(books):
            authors_full_names = book.authors.split('/')
            authors = []
            for full_name in authors_full_names:
                author, _ = Author.objects.get_or_create(full_name=full_name)
                authors.append(author.id)

            book = Book.objects.create(
                title=book.title,
                isbn=book.isbn,
                isbn13=book.isbn13,
                num_pages=book.num_pages,
                publication_date=datetime.strptime(book.publication_date, '%m/%d/%Y').date(),
            )
            book.authors.add(*authors)

            if idx % (len(books) // 10) == 0:
                print(f'{idx // (len(books) // 10) * 10}%')
