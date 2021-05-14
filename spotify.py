from moodify import Moodify
from album import Album
from track import Track
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from dataclasses import asdict
from typing import Dict, List, Any

import random

class SpotifyService():
    def __init__(self, scope) -> None:
        self.scope = scope
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        self.saved_tracks = [*self.current_user_saved_tracks(), *self.current_user_saved_album_tracks(),
                             *self.get_recently_played()]
        self.saved_tracks_audio_analysis = self.get_audio_analysis()

    def get_recently_played(self) -> List[Dict]:
        r = self.spotify.current_user_recently_played(limit=50)
        saved_tracks = []
        for idx, item in enumerate(r['items']):
            track_dict = asdict(self._create_track(item))
            saved_tracks.append(track_dict)
        return saved_tracks
    
    def current_user_saved_tracks(self) -> List[Dict]:
        r = self.spotify.current_user_saved_tracks(limit=50)
        saved_tracks = []
        for idx, item in enumerate(r['items']):
            track_dict = asdict(self._create_track(item))
            saved_tracks.append(track_dict)
        return saved_tracks
    
    def current_user_saved_album_tracks(self)-> Dict:
        r = self.spotify.current_user_saved_albums(limit=50)
        saved_tracks = []
        for idx, album_item in enumerate(r['items']):
            album_item = album_item['album']
            album = Album(album_name=album_item['name'],
                          tracks=self._create_tracks_from_album(album_item))
            saved_tracks += [asdict(track) for track in album.tracks]
        return saved_tracks
        
    def get_audio_analysis(self, limit=50, track_ids=None)-> Dict:
        if track_ids==None:
            track_ids = [track['track_uri'] for track in self.saved_tracks] 
            r = self.spotify.audio_features(tracks=track_ids[:limit])
            saved_tracks_audio_analysis = saved_tracks_audio_analysis = dict(zip(track_ids, r))
        else:
            r = self.spotify.audio_features(tracks=track_ids)
            saved_tracks_audio_analysis = dict(zip(track_ids, r))
        return saved_tracks_audio_analysis

    def get_saved_tracks(self):
        return self.saved_tracks
    
    def create_playlist(self, name, max_valence, min_valence, num_tracks):
        moodify = Moodify()
        filtered_tracks = moodify.filter_tracks_for_mood(self.saved_tracks_audio_analysis, max_valence, min_valence, num_tracks)
        p_response = self.spotify.user_playlist_create(user='caitray1', name=name, public=True, collaborative=False, description='Testing')
        playlist_id = p_response['id']
        self._add_songs_to_playlist(playlist_id=playlist_id, items=filtered_tracks)
        return p_response
    
    def _add_songs_to_playlist(self, playlist_id, items):
        return self.spotify.playlist_add_items(playlist_id, items, position=None)

    def _create_track(self, item):
        track = Track(track_id=item['track']['id'],
                      track_uri=item['track']['uri'],
                      track_name=item['track']['name'],
                      artist_id=item['track']['artists'][0]['id'],
                      artist_uri=item['track']['artists'][0]['uri'],
                      artist_name=item['track']['artists'][0]['name'],
                      popularity=item['track']['popularity'],
                      duration_ms=item['track']['duration_ms'])
        return track
    
    def _create_tracks_from_album(self, album_item):
        tracks = []
        for track_idx in range(album_item['total_tracks']):
            track = Track(track_id=album_item['tracks']['items'][track_idx]['id'],
                        track_uri=album_item['tracks']['items'][track_idx]['uri'],
                        track_name=album_item['tracks']['items'][track_idx]['name'],
                        artist_id=album_item['artists'][0]['id'],
                        artist_uri=album_item['artists'][0]['uri'],
                        artist_name=album_item['artists'][0]['name'])
            tracks.append(track)
        return tracks

