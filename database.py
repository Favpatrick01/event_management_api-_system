from schemas.user import User
from schemas.event import Event
from schemas.speaker import Speaker
from schemas.registration import Registration
from typing import Dict

user_db: dict[str, User] = {}

event_db: dict[str, Event] = {}

speaker_db = {}

registrations_db: Dict[str, Registration] = {}

