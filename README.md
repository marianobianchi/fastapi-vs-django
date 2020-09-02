# Dataset

Books dataset was downloaded from https://www.kaggle.com/jealousleopard/goodreadsbooks


# Database
To narrow the functionality of this comparison I won't use all data in the dataset. I will just store authors info, publisher and minimal book information

## Fixes
- There were some authors that contained a comma (",") in its name, so I had to clean them.
- There were two invalid publication dates: 11/31/2000 and 6/31/1982


## Author

Fields:
- full_name


## Book

Fields:
- title
- isbn
- isbn13
- num_pages
- publication_date


## BookAuthors
It is a many-to-many relation between book and author
Fields:
- Author
- Book


# API

## List of books
- Endpoint that returns a list of books
- Paginated, 30 books per page
- filter by title
- public endpoint

## Book detail
- given a book id, returns all details from that book
- public endpoint

## Create book
- title is mandatory
- other fields are optional
- need permission to create book

## Edit (put/patch) book
- every field can be edited
- need permission to edit book


# FastAPI

* It wasn't obvious how to handle a ManyToMany relation using pydantic. It wasn't in the docs. I had to search and found a clue in some github issue.
* I got a Pydantic.errors.ConfigError: field "authors" not yet prepared so type is still a ForwardRef, you might need to call Book.update_forward_refs()
