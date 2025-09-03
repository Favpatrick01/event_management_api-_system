from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Union

class Event(BaseModel):
    id: str
    title: str
    location: str
    speaker_name: str
    speaker_topic: str
    is_open: bool
    date: date
    created_by: str  # <-- NEW FIELD to track event owner

class EventCreate(BaseModel):
    title: str
    location: str
    speaker_name: str
    speaker_topic: str
    is_open: bool
    date: date
    created_by: Optional[str] = None  # <-- NEW FIELD, assigned at runtime

class EventUpdate(BaseModel):
    title: str
    location: str
    speaker_name: str
    speaker_topic: str
    is_open: bool
    date: date

class CloseEventReg(BaseModel):
    is_open: bool = False

class Events(BaseModel):
    event: List[Event]

class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Union[Event, Events]] = None