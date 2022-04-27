import random

from lda_model import LdaModel
from record_collection import RecordCollection
from spotify import SpotifyService


class Selecta:
    """Personalization logic."""
    def __init__(self, spotifyService: SpotifyService, recordCollection: RecordCollection) -> None:
        self.spotifyService = spotifyService
        self.recordCollection = recordCollection

    def create_moody_playlist(self, playlist_name, max_valence, min_valence, num_tracks):
        """
        Recommend songs based on Spotify given label; valence.
        :param playlist_name:
        playlist_name: str
        :param max_valence:
        max_valence: int
        :param min_valence:
        min_valence: int
        :param num_tracks:
        num_tracks: int
        :return:
        track_uris: List[str]
        """
        saved_tracks = self.recordCollection.tracks
        saved_tracks_audio_analysis = self.spotifyService.get_audio_features(saved_tracks)
        filtered_tracks = []
        for track in saved_tracks_audio_analysis.keys():
            valence = float(saved_tracks_audio_analysis[track]['valence'])
            if (valence >= float(min_valence)) & (valence <= float(max_valence)):
                filtered_tracks.append(track)
        tracks_to_add_to_playlist = random.sample(filtered_tracks, min(num_tracks, len(filtered_tracks)))
        return self.spotifyService.make_playlist(playlist_name, tracks_to_add_to_playlist)
    
    def create_similar_lyrics_playlist(self, spotify_id, track_name, artist_name, num_tracks):
        """
        Recommend songs based on topic similarity using LDA.
        :param track_name:
        track_name: str
        :param artist_name:
        artist_name: str
        :param num_tracks:
        num_tracks: int
        :return:
        track_uris: List[str]
        """
        if self.recordCollection.record_in_collection(track_name, artist_name):
            lda = LdaModel(self.recordCollection)
            track_recommendation_uris = lda.get_recommendations(track_name, artist_name, num_tracks)
            playlist_name = f"Similar to {track_name} by {artist_name}"
            return self.spotifyService.make_playlist(spotify_id, playlist_name, track_recommendation_uris)
        else:
            return "This record isn't in the collection, please choose another."