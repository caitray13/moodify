from dataclasses import dataclass, asdict, field
from typing import Dict, List

from spotify import SpotifyService

from track import Track


@dataclass
class RecordCollection:
    spotifyService: SpotifyService
    tracks: List[Track] = field(init=False)

    def __post_init__(self) -> None:
        self._build_collection()

    def _build_collection(self):
        self.tracks = [*self.spotifyService.current_user_saved_tracks(),
                       *self.spotifyService.current_user_saved_album_tracks(),
                       *self.spotifyService.current_user_recently_played()]

    def get_tracks(self) -> List[Dict]:
        return [asdict(track) for track in self.tracks]
    
    def __str__(self):
        return f"Record collection made up of {len(self.tracks)} songs."




