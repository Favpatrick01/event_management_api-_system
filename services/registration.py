from uuid import uuid4, UUID
from datetime import date
from fastapi import HTTPException
from database import registrations_db, event_db, user_db
from schemas.registration import Registration, RegistrationCreate


class RegistrationService:

    @staticmethod
    def register_user_for_event(event_id: UUID, user_id: UUID) -> Registration:
        # Validate user
        user = user_db.get(str(user_id))
        if not user or not user.is_active:
            raise HTTPException(status_code=403, detail="User is not active or does not exist")

        # Validate event
        event = event_db.get(str(event_id))
        if not event or not event.is_open:
            raise HTTPException(status_code=400, detail="Event is not open for registration")

        # Prevent duplicate registration
        for reg in registrations_db.values():
            if reg.user_id == user_id and reg.event_id == event_id:
                raise HTTPException(status_code=400, detail="User already registered for this event")

        # Create registration
        registration = Registration(
            id=uuid4(),
            user_id=user_id,
            event_id=event_id,
            registration_date=date.today(),
            attended=False
        )

        registrations_db[str(registration.id)] = registration
        return registration

    @staticmethod
    def mark_attendance(registration_id: UUID) -> Registration:
        registration = registrations_db.get(str(registration_id))
        if not registration:
            raise HTTPException(status_code=404, detail="Registration not found")

        updated_registration = registration.copy(update={"attended": True})
        registrations_db[str(registration_id)] = updated_registration
        return updated_registration

    @staticmethod
    def get_registrations_by_user(user_id: UUID):
        return [reg for reg in registrations_db.values() if reg.user_id == user_id]

    @staticmethod
    def get_all_registrations():
        return list(registrations_db.values())