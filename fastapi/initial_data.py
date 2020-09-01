from datetime import datetime

from book_csv_reader import get_books
from sql_app.crud import create_author, create_book, get_author_by_name
from sql_app.database import SessionLocal
from sql_app.schemas import AuthorCreate, BookCreate

db = SessionLocal()
try:
    books = get_books()
    for idx, book in enumerate(books):
        authors_full_names = book.authors.split('/')
        authors_ids = []
        for full_name in authors_full_names:
            existing_author = get_author_by_name(db, full_name)
            if existing_author:
                authors_ids.append(existing_author[0].id)
            else:
                db_author = create_author(db, AuthorCreate(full_name=full_name))
                authors_ids.append(db_author.id)

        schema_book = BookCreate(
            title=book.title,
            isbn=book.isbn,
            isbn13=book.isbn13,
            num_pages=book.num_pages,
            publication_date=datetime.strptime(book.publication_date, '%m/%d/%Y').date(),
            authors=authors_ids,
        )
        create_book(db, schema_book)

        if idx % (len(books) // 10) == 0:
            print(f'{idx // (len(books) // 10) * 10}%')
finally:
    db.close()
