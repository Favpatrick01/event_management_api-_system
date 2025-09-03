from uuid import UUID, uuid4
from typing import Optional

from fastapi import HTTPException
from database import event_db
from schemas.event import Event, EventCreate, EventUpdate, CloseEventReg


class EventService:

    @staticmethod
    def add_event(event_in: EventCreate) -> Event:
        event = Event(
            id=str(uuid4()),
            **event_in.model_dump()
        )
        event_db[event.id] = event
        return event


    @staticmethod
    def _get_event_if_owner(event_id: UUID, user_id: UUID) -> Event:
        """
        Retrieve an event if the user is the owner.
        """
        print(f"Looking for event_id: {event_id} for user_id: {user_id}")
        
        event = event_db.get(str(event_id))
        if not event:
            print("Event not found!")
            raise HTTPException(status_code=404, detail="Event not found")
        
        print(f"Event found: {event}")
        if event.created_by != str(user_id):
            print(f"Unauthorized access by {user_id}")
            raise HTTPException(status_code=403, detail="Unauthorized action")
        
        return event


    @staticmethod
    def update_event(event_id: str, event_in: EventUpdate, user_id: str) -> Optional[Event]:
        event = EventService._get_event_if_owner(event_id, user_id)
        if not event:
            return None

        update_data = event_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(event, field, value)

        event_db[event_id] = event
        return event

    @staticmethod
    def close_event_registration(event_id: str, event_in: CloseEventReg, user_id: str) -> Optional[Event]:
        event = EventService._get_event_if_owner(event_id, user_id)
        if not event:
            return None

        event.is_open = event_in.is_open
        event_db[event_id] = event
        return event

    @staticmethod
    def delete_event(event_id: str, user_id: str) -> bool:
        event = EventService._get_event_if_owner(event_id, user_id)
        if not event:
            return False

        del event_db[event_id]
        return True


event_services = EventService()