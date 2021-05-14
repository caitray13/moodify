from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass
class Track():
    """ Object class for represeting a track on Spotify"""
    track_id: str
    track_uri: str
    track_name: str
    artist_name: str
    artist_id: str
    artist_uri: str
    popularity: str = field(default=None)
    duration_ms: float = field(default=None)

    def __str__(self):
        return f"{self.track_name} by {self.artist_name}"