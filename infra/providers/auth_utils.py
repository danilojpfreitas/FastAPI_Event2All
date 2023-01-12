from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from infra.providers import token_provider
from jose import JWTError
from user.models.get_user import UserResponseModel

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')


def search_user_by_email(email: str, db) -> UserResponseModel:
    user = db.query(UserResponseModel).filter(
        UserResponseModel.email == email
    ).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def get_log_user(token: str = Depends(oauth2_schema),
                 session: Session = Depends(get_db)):
    exception = HTTPException(status_code=401, detail='Token invalid')
    try:
        email = token_provider.check_access_token(token)
    except JWTError:
        raise exception
    if not email:
        raise exception
    user = UserResponseModel(session).search_user_by_email(email)
    if not user:
        raise exception
    return user
