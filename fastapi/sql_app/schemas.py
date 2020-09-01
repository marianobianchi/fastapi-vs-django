from datetime import date
from typing import List, Optional, ForwardRef

from pydantic import BaseModel


class AuthorBase(BaseModel):
    full_name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    title: str
    isbn: Optional[str] = None
    isbn13: Optional[str] = None
    num_pages: Optional[int] = None
    publication_date: Optional[date] = None


class BookCreate(BookBase):
    authors: Optional[List[int]] = []


class BookUpdate(BookCreate):
    title: Optional[str] = None


class Book(BookBase):
    id: int

    authors: List[Author] = []

    class Config:
        orm_mode = True
