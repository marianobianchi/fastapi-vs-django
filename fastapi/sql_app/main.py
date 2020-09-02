from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from . import auth, crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post('/token')
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    FAIL_LOGIN_MSG = 'Incorrect username or password'
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=FAIL_LOGIN_MSG)

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    return current_user


@app.post('/books/', response_model=schemas.Book)
async def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user)
):
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail='Book title already exists')
    return crud.create_book(db=db, book=book)


@app.patch('/books/{book_id}', response_model=schemas.Book)
async def update_book(
    book_id: int,
    book: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(auth.get_current_active_user),
):
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail='Book does not exists')
    return crud.update_book(db=db, db_book=db_book, book=book)


@app.get('/books/', response_model=List[schemas.Book])
async def read_books(title: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, title=title, skip=skip, limit=limit)
    return books


@app.get('/books/{book_id}', response_model=schemas.Book)
async def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail='Book does not exists')
    return db_book
