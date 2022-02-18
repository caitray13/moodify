import random

from record_collection import RecordCollection
from spotify import SpotifyService


class Selector:
    """Personalization logic."""
    def __init__(self, spotifyService: SpotifyService, recordCollection: RecordCollection) -> None:
        self.spotifyService = spotifyService
        self.recordCollection = recordCollection

    def create_moody_playlist(self, playlist_name, max_valence, min_valence, num_tracks):
        saved_tracks = self.recordCollection.tracks
        saved_tracks_audio_analysis = self.spotifyService.get_audio_features(saved_tracks)
        filtered_tracks = []
        for track in saved_tracks_audio_analysis.keys():
            valence = float(saved_tracks_audio_analysis[track]['valence'])
            if (valence >= float(min_valence)) & (valence <= float(max_valence)):
                filtered_tracks.append(track)
        tracks_to_add_to_playlist = random.sample(filtered_tracks, min(int(num_tracks), len(filtered_tracks)))
        return self.spotifyService.make_playlist(playlist_name, tracks_to_add_to_playlist)
