from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, BaseConfig
from typing import List, Optional
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from user.models.get_user import UserResponseModel
from datetime import datetime
from infra.providers import hash_provider, token_provider, auth_utils
from event.models.event_model import EventModel

BaseConfig.arbitrary_types_allowed = True

router = APIRouter(prefix="/user")


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserResponse(OurBaseModel):
    id: int
    name: str
    email: str
    birth_date: str
    createdAt: datetime = datetime.now()
    updatedAt: datetime = datetime.now()


class UserRequest(OurBaseModel):
    name: str
    email: str
    birth_date: str
    password: str


class LoginData(OurBaseModel):
    email: str
    password: str


class LoginOK(OurBaseModel):
    user: UserRequest
    access_token: str


@router.get("", response_model=List[UserResponse], tags=["User"], status_code=200)
def get_user(db: Session = Depends(get_db)) -> List[UserResponse]:
    return db.query(UserResponseModel).all()


@router.get("/{id}", response_model=UserResponse, tags=["User"], status_code=200)
def get_user_by_id(user_by_id: int,
                   db: Session = Depends(get_db)) -> List[UserResponse]:
    return search_user_by_id(user_by_id, db)


@router.post("", response_model=UserResponse, tags=["User"], status_code=201)
def post_user(user_request: UserRequest,
              db: Session = Depends(get_db)) -> UserResponse:
    # Check Email
    if check_email(user_request.email, db) is not None:
        raise HTTPException(status_code=409, detail="Email already exists")

    # New User
    user_request.password = hash_provider.generate_hash(user_request.password)

    user = UserResponseModel(
        name=user_request.email, email=user_request.email, birth_date=user_request.birth_date,
        password=user_request.password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/{id}", response_model=UserResponse, tags=["User"], status_code=200)
def put_user(id: int,
             user_request: UserRequest,
             db: Session = Depends(get_db)) -> UserResponse:

    # Check Email
    if check_email(user_request.email, db) is not None:
        raise HTTPException(status_code=409, detail="Email already exists")

    user = search_user_by_id(id, db)

    user.name = user_request.name
    user.email = user_request.email
    user.birth_date = user_request.birth_date
    user.password = hash_provider.generate_hash(user_request.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{id}", tags=["User"], status_code=204)
def delete_user(id: int,
                db: Session = Depends(get_db)) -> None:
    user = search_user_by_id(id, db)

    db.delete(user)
    db.commit()


# Auth

@router.post("/login", tags=["Auth"], status_code=201)
def auth_user(login_data: LoginData, db: Session = Depends(get_db)):
    password = login_data.password
    email = login_data.email

    user = search_user_by_email(email, db)

    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    validate_password = hash_provider.check_hash(password, user.password)

    if not validate_password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Token JWT
    token = token_provider.new_access_token({'sub': user.email})
    return LoginOK(user=user, access_token=token)


# @router.get('/me', response_model=UserRequest)
# def me(user: UserResponseModel = Depends(auth_utils.get_log_user)):
#    return user


def check_email(email: str, db) -> UserResponseModel:
    user = db.query(UserResponseModel).filter(
        UserResponseModel.email == email
    ).first()

    return user


def search_user_by_email(email: str, db) -> UserResponseModel:
    user = check_email(email, db)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def search_user_by_id(user_by_id: int, db: Session) -> UserResponseModel:
    user = db.query(UserResponseModel).get(user_by_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
