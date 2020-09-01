from csv import DictReader
from collections import namedtuple

Book = namedtuple('Book', [
    'bookID',
    'title',
    'authors',
    'average_rating',
    'isbn',
    'isbn13',
    'language_code',
    'num_pages',
    'ratings_count',
    'text_reviews_count',
    'publication_date',
    'publisher',
])


def get_books(fname='books.csv'):
    books = []
    with open(fname, 'r') as f:
        reader = DictReader(f)
        for line_dict in reader:
            books.append(Book(**line_dict))

    return books
