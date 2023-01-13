from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from shared.dependencies import get_db
from datetime import datetime
from infra.providers import hash_provider, token_provider, auth_utils
from event.models.event_model import EventModel
from user.models.get_user import UserResponseModel

router = APIRouter(prefix="/event")


class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True


class EventResponse(OurBaseModel):
    id: int
    place: str
    name: str
    date: str
    managers: str
    invite_number: int
    event_budget: int
    user_id: Optional[int]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class EventRequest(OurBaseModel):
    place: str
    name: str
    date: str
    managers: str
    invite_number: int
    event_budget: int
    user_id: Optional[int]
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


@router.get("", response_model=List[EventResponse], tags=["Event"], status_code=200)
def get_event(db: Session = Depends(get_db)) -> List[EventResponse]:
    return db.query(EventModel).all()


@router.get("/{id_user}", response_model=List[EventResponse], tags=["Event"], status_code=200)
def get_events_by_user_id(id_user: int,
                          db: Session = Depends(get_db)) -> List[EventResponse]:
    return search_event_by_user_id(id_user, db)


@router.post("", response_model=EventResponse, tags=["Event"], status_code=201)
def post_event(event_request: EventRequest,
               db: Session = Depends(get_db)) -> EventResponse:
    exist_user_id(event_request.user_id, db)

    event = EventModel(
        **event_request.dict()
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def exist_user_id(user_id, db):
    if user_id is not None:
        event = db.query(UserResponseModel).get(user_id)
        if event is None:
            raise HTTPException(status_code=422, detail="User not found")


def search_event_by_user_id(user_by_id: int, db: Session) -> List[EventModel]:
    event = db.query(EventModel).filter(EventModel.user_id == user_by_id).all()

    if event is None:
        raise HTTPException(status_code=404, detail="User not found")

    return event


