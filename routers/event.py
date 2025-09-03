from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID, uuid4
from database import event_db, user_db
from schemas.event import EventCreate, EventUpdate, CloseEventReg, Response, Event
from services.event import event_services

event_router = APIRouter()

# Dependency to check if user exists
def get_current_user(user_id: str):
    user = user_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found or not registered")
    return user

# Get all events
@event_router.get("", response_model=Response, tags=["Events"])
def get_event():
    return Response(
        message="Events retrieved successfully",
        data={"event": list(event_db.values())}
    )

# Add event - only for registered users
@event_router.post("", response_model=Response, tags=["Events"])
def add_event(event_in: EventCreate, user=Depends(get_current_user)):
    # Ensure created_by matches current user
    event_in.created_by = user.id
    event = event_services.add_event(event_in)
    return Response(message="Event added successfully", data=event)

# Update event
@event_router.put("/{id}", response_model=Response, tags=["Events"])
def update_event(id: UUID, event_in: EventUpdate, user=Depends(get_current_user)):
    event = event_services.update_event(str(id), event_in, user.id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID: {id} not found or unauthorized")
    return Response(message="Event updated successfully", data=event)

# Close event registration
@event_router.patch("/{id}", response_model=Response, tags=["Events"])
def close_event_registration(id: UUID, event_in: CloseEventReg, user=Depends(get_current_user)):
    event = event_services.close_event_registration(str(id), event_in, user.id)
    if not event:
        raise HTTPException(status_code=404, detail=f"Event with ID: {id} not found or unauthorized")
    return Response(message="Event closed successfully", data=event)

# Delete event
@event_router.delete("/{id}", response_model=Response, tags=["Events"])
def delete_event(id: UUID, user=Depends(get_current_user)):
    is_deleted = event_services.delete_event(str(id), user.id)
    if not is_deleted:
        raise HTTPException(status_code=404, detail=f"Event with ID: {id} not found or unauthorized")
    return Response(message="Event deleted successfully")