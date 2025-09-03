from fastapi import APIRouter, HTTPException, Query, Body
from schemas.speaker import SpeakerCreate, SpeakerUpdate, Response, Speakers
from services.speaker import SpeakerService

speaker_router = APIRouter()

# Create a speaker
@speaker_router.post("", response_model=Response, tags=["Speakers"])
def create_speaker(user_id: str = Query(...), speaker_in: SpeakerCreate = Body(...)):
    speaker = SpeakerService.add_speaker(user_id, speaker_in)
    if not speaker:
        raise HTTPException(status_code=400, detail="Failed to create speaker. User may not be registered.")
    return Response(message="Speaker created successfully", data=speaker)

# Get all speakers
@speaker_router.get("", response_model=Response, tags=["Speakers"])
def get_speakers():
    speakers = SpeakerService.get_all_speakers()
    return Response(message="Speakers retrieved successfully", data=Speakers(speakers=speakers))

# Get a single speaker by name
@speaker_router.get("/{name}", response_model=Response, tags=["Speakers"])
def get_speaker(name: str):
    speaker = SpeakerService.get_speaker_by_name(name)
    if not speaker:
        raise HTTPException(status_code=404, detail=f"Speaker with name '{name}' not found")
    return Response(message="Speaker retrieved successfully", data=speaker)

# Update a speaker
@speaker_router.put("/{speaker_id}", response_model=Response, tags=["Speakers"])
def update_speaker(
    speaker_id: str,
    user_id: str = Query(...),
    speaker_in: SpeakerUpdate = Body(...)
):
    speaker = SpeakerService.update_speaker(user_id, speaker_id, speaker_in)
    if not speaker:
        raise HTTPException(status_code=404, detail=f"Speaker with ID '{speaker_id}' not found or unauthorized")
    return Response(message="Speaker updated successfully", data=speaker)

# Delete a speaker
@speaker_router.delete("/{speaker_id}", response_model=Response, tags=["Speakers"])
def delete_speaker(speaker_id: str, user_id: str = Query(...)):
    deleted = SpeakerService.delete_speaker(user_id, speaker_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Speaker with ID '{speaker_id}' not found or unauthorized")
    return Response(message="Speaker deleted successfully")