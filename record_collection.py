from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional

from spotify import SpotifyService

from track import Track


@dataclass
class RecordCollection:
    tracks: Optional[List[Track]] = field(default_factory=list)

    def build_collection(self, spotifyService):
        self.tracks = [*self.spotifyService.current_user_saved_tracks(),
                       *self.spotifyService.current_user_saved_album_tracks(),
                       *self.spotifyService.current_user_recently_played()]

    def get_tracks(self) -> List[Dict]:
        return [asdict(track) for track in self.tracks]
    
    def __str__(self):
        return f"Record collection made up of {len(self.tracks)} songs."




