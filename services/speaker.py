from uuid import uuid4
from typing import List
from fastapi import HTTPException
from database import speaker_db, user_db
from schemas.speaker import Speaker, SpeakerCreate, SpeakerUpdate


class SpeakerService:
    @staticmethod
    def validate_user(user_id: str):
        """Ensure the user is registered."""
        if user_id not in user_db:
            raise HTTPException(status_code=403, detail="User not registered")

    @staticmethod
    def validate_unique(name: str, topic: str, exclude_id: str = None):
        """
        Ensure no duplicate speaker exists with the same name and topic.
        Case-insensitive and whitespace-trimmed.
        """
        name = name.strip().lower()
        topic = topic.strip().lower()
        for s in speaker_db.values():
            if s.id == exclude_id:
                continue
            if s.name.strip().lower() == name and s.topic.strip().lower() == topic:
                raise HTTPException(
                    status_code=400,
                    detail=f"Speaker '{name}' already registered for topic '{topic}'."
                )

    @staticmethod
    def add_speaker(user_id: str, speaker_in: SpeakerCreate) -> Speaker:
        """Add a new speaker."""
        SpeakerService.validate_user(user_id)
        SpeakerService.validate_unique(speaker_in.name, speaker_in.topic)

        speaker = Speaker(
            id=str(uuid4()),
            created_by=user_id,
            **speaker_in.model_dump()
        )
        speaker_db[speaker.id] = speaker
        return speaker

    @staticmethod
    def get_all_speakers() -> List[Speaker]:
        """Retrieve all speakers."""
        return list(speaker_db.values())

    @staticmethod
    def get_speaker_by_id(speaker_id: str) -> Speaker:
        """Retrieve a speaker by ID."""
        speaker = speaker_db.get(speaker_id)
        if not speaker:
            raise HTTPException(status_code=404, detail="Speaker not found")
        return speaker

    @staticmethod
    def get_speaker_by_name(name: str) -> Speaker:
        """Retrieve a speaker by name (case-insensitive)."""
        name = name.strip().lower()
        for speaker in speaker_db.values():
            if speaker.name.strip().lower() == name:
                return speaker
        raise HTTPException(status_code=404, detail=f"Speaker with name '{name}' not found")

    @staticmethod
    def update_speaker(user_id: str, speaker_id: str, speaker_in: SpeakerUpdate) -> Speaker:
        """Update a speaker if the user owns it."""
        SpeakerService.validate_user(user_id)
        speaker = SpeakerService.get_speaker_by_id(speaker_id)

        # Enforce ownership
        if speaker.created_by != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized action")

        updated_name = speaker_in.name or speaker.name
        updated_topic = speaker_in.topic or speaker.topic
        SpeakerService.validate_unique(updated_name, updated_topic, exclude_id=speaker_id)

        updated_speaker = speaker.copy(update=speaker_in.model_dump(exclude_unset=True))
        speaker_db[speaker_id] = updated_speaker
        return updated_speaker

    @staticmethod
    def delete_speaker(user_id: str, speaker_id: str) -> dict:
        """Delete a speaker if the user owns it."""
        SpeakerService.validate_user(user_id)
        speaker = SpeakerService.get_speaker_by_id(speaker_id)

        # Enforce ownership
        if speaker.created_by != user_id:
            raise HTTPException(status_code=403, detail="Unauthorized action")

        del speaker_db[speaker_id]
        return {"success": True, "message": f"Speaker '{speaker.name}' deleted successfully."}