from dataclasses import dataclass, asdict
from typing import Dict, List

from spotify import SpotifyService

from track import Track


@dataclass
class RecordCollection:
    __tracks: List[Track]

    def __init__(self, spotifyService: SpotifyService) -> None:
        self.spotifyService = spotifyService
        self._build_collection()

    def _build_collection(self):
        self.tracks = [*self.spotifyService.current_user_saved_tracks(),
                       *self.spotifyService.current_user_saved_album_tracks(),
                       *self.spotifyService.current_user_recently_played()]

    def get_tracks(self) -> List[Dict[Track]]:
        return [asdict(track) for track in self.__tracks]




