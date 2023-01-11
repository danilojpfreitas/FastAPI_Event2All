from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/user")


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    password: str
    createdAt: int
    updatedAt: int

class UserRequest(BaseModel):
    name: str
    email: str
    password: str
    createdAt: int
    updatedAt: int


@router.get("", response_model=List[UserResponse])
def get_user():
    return [
        UserResponse
    ]

@router.post("", response_model=List[UserRequest], status_code=201)
def post_user(conta: UserRequest):
    return None
