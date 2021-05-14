from dataclasses import dataclass
from track import Track
from typing import List

@dataclass
class Album():
    """ Object class for represeting an album on Spotify"""
    album_name: str
    tracks: List[Track]