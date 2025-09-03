from uuid import UUID
from datetime import date
from typing import Optional, List, Union
from pydantic import BaseModel, Field


class Registration(BaseModel):
    id: UUID
    user_id: UUID
    event_id: UUID
    registration_date: date = Field(default_factory=date.today)
    attended: bool = False


class RegistrationCreate(BaseModel):
    user_id: UUID


class RegistrationUpdate(BaseModel):
    attended: Optional[bool] = None


class Registrations(BaseModel):
    registrations: List[Registration]


class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Union[Registration, Registrations]] = None
