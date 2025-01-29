from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Video(BaseModel):
    title: str
    path: str  # Path to the video file or URL

class Subtitle(BaseModel):
    title: str
    videos: List[Video] = []
    subtitles: Optional[List['Subtitle']] = []  # Nested subtitles

class Course(BaseModel):
    title: str
    description: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    subtitles: List[Subtitle] = []