from pydantic import BaseModel
from typing import Optional, List, Union

class Speaker(BaseModel):
    id: str
    name: str
    topic: str
    created_by: str

class SpeakerCreate(BaseModel):
    name: str
    topic: str

class SpeakerUpdate(BaseModel):
    name: Optional[str] = None 
    topic: Optional[str] = None

class Speakers(BaseModel):
    speakers: List[Speaker]  
class Response(BaseModel):
    message: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None
    data: Optional[Union[Speaker, Speakers]] = None