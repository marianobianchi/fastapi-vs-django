from sqlalchemy.orm import Session

from . import models, schemas


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()


def get_books(
    db: Session,
    title: str = None,
    skip: int = 0,
    limit: int = 30
):
    base_query = None
    if title is None:
        base_query = db.query(models.Book)
    else:
        base_query = db.query(models.Book)\
                       .filter(models.Book.title.like(f'%{title}%'))
    return base_query.order_by(models.Book.id).offset(skip).limit(limit).all()


def _commit_book(db: Session, db_book: models.Book, data: dict):
    for field_name, value in data.items():
        if field_name == 'authors':
            db_authors = db.query(models.Author)\
                           .filter(models.Author.id.in_(value))\
                           .all()
            setattr(db_book, field_name, db_authors)
        else:
            setattr(db_book, field_name, value)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def create_book(db: Session, book: schemas.BookCreate):
    return _commit_book(db, models.Book(), book.dict())


def update_book(db: Session, db_book: models.Book, book: schemas.BookUpdate):
    return _commit_book(db, db_book, book.dict(exclude_unset=True))


def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_by_name(db: Session, name: str):
    return db.query(models.Author)\
             .filter(models.Author.full_name.like(f'%{name}%'))\
             .all()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User)\
             .filter(models.User.username == username)\
             .first()
