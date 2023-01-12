from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from user.models.get_user import UserResponseModel

router = APIRouter(prefix="/user")


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class UserResponse(OurBaseModel):
    id: int
    name: str
    email: str
    password: str

#    createdAt: int
#    updatedAt: int


class UserRequest(OurBaseModel):
    name: str
    email: str
    password: str


@router.get("", response_model=List[UserResponse], status_code=200)
def get_user(db: Session = Depends(get_db)) -> List[UserResponse]:
    return db.query(UserResponseModel).all()


@router.post("", response_model=UserResponse, status_code=201)
def post_user(user_request: UserRequest,
              db: Session = Depends(get_db)) -> UserResponse:
    user = UserResponseModel(
        **user_request.dict()
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
