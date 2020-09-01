from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/books/', response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail='Book title already exists')
    return crud.create_book(db=db, book=book)


@app.patch('/books/{book_id}', response_model=schemas.Book)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail='Book does not exists')
    return crud.update_book(db=db, db_book=db_book, book=book)


@app.get('/books/', response_model=List[schemas.Book])
def read_books(title: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, title=title, skip=skip, limit=limit)
    return books


@app.get('/books/{book_id}', response_model=schemas.Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail='Book does not exists')
    return db_book


@app.post('/authors/', response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_name(db, name=author.full_name)
    if db_author:
        raise HTTPException(status_code=400, detail='Author already exists')
    return crud.create_author(db=db, author=author)


@app.get('/authors/', response_model=List[schemas.Author])
def read_author(name: str, db: Session = Depends(get_db)):
    authors = crud.get_author_by_name(db, name=name)
    return authors


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items
