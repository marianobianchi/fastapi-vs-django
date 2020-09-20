from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import crud, database, models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_hash_password(password: str):
    return password


def verify_password(db_user: models.User, password: str):
    return db_user.hashed_password == fake_hash_password(password)


def authenticate_user(db: Session, username: str, password: str):
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        return None

    if not verify_password(db_user, password):
        return None

    return schemas.User(**db_user.__dict__)


def get_user(db: Session, username: str):
    db_user = crud.get_user_by_username(db, username)
    if db_user:
        return schemas.UserInDB(**db_user.__dict__)


def fake_decode_token(db: Session, token: str):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(db, token)
    return user


async def get_current_user(
    db: Session = Depends(database.get_db),
    token: str = Depends(oauth2_scheme),
):
    user = fake_decode_token(db, token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user)
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
