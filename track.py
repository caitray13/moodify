from dataclasses import dataclass, field
from typing import Any, Optional, List


@dataclass
class Track:
    """ Object class for represeting a track on Spotify"""
    track_uri: str
    track_name: str
    artist_name: str
    lyrics: Optional[List[str]] = field(default_factory=list)
    track_id: Optional[str] = None
    artist_id: Optional[str] = None
    artist_uri: Optional[str] = None
    popularity: str = field(default=None)
    duration_ms: float = field(default=None)

    def __str__(self):
        return f"{self.track_name} by {self.artist_name}"
