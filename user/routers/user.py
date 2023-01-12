from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from user.models.get_user import UserResponseModel
from datetime import datetime

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
    user = UserResponseModel(
        **user_request.dict()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@router.put("/{id}", response_model=UserResponse, tags=["User"], status_code=200)
def put_user(id: int,
             user_request: UserRequest,
             db: Session = Depends(get_db)) -> UserResponse:
    user = search_user_by_id(id, db)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = user_request.name
    user.email = user_request.email
    user.birth_date = user.birth_date
    user.password = user_request.password

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


def search_user_by_id(user_by_id: int, db: Session) -> UserResponseModel:
    user = db.query(UserResponseModel).get(user_by_id)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user
