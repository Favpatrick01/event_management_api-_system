from uuid import UUID
from fastapi import APIRouter
from schemas.registration import Response, RegistrationCreate, Registrations
from services.registration import RegistrationService

registration_router = APIRouter()

# Register a user for an event
@registration_router.post("/events/{event_id}/register", response_model=Response)
def register_user_for_event(event_id: UUID, payload: RegistrationCreate):
    registration = RegistrationService.register_user_for_event(event_id, payload.user_id)
    return Response(message="User registered successfully", data=registration)

# Mark attendance for a registration
@registration_router.patch("/{registration_id}/attend", response_model=Response)
def mark_attendance(registration_id: UUID):
    registration = RegistrationService.mark_attendance(registration_id)
    return Response(message="Attendance marked successfully", data=registration)

# Get all registrations (for all users)
@registration_router.get("/all", response_model=Response)
def get_all_registrations():
    registrations = RegistrationService.get_all_registrations()
    return Response(message="All registrations retrieved", data=Registrations(registrations=registrations))

# Get registrations for a specific user
@registration_router.get("/user/{user_id}", response_model=Response)
def get_user_registrations(user_id: UUID):
    registrations = RegistrationService.get_registrations_by_user(user_id)
    return Response(message=f"Registrations for user {user_id}", data=Registrations(registrations=registrations))