from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from track import Track

LIMIT = 50


def chunks(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


class SpotifyService:
    def __init__(self, scope):
        self.scope = scope
        self.spotipyClient = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=self.scope))

    def current_user_recently_played(self) -> List[Track]:
        """
        Returns users last 50 listened to tracks.
        :return:
        saved_tracks: List[Track]
        """
        r = self.spotipyClient.current_user_recently_played(limit=LIMIT)
        saved_tracks = []
        for idx, item in enumerate(r['items']):
            track = self._create_track(item)
            saved_tracks.append(track)
        return saved_tracks

    def current_user_saved_tracks(self) -> List[Track]:
        """
        Returns the user's last 50 saved tracks.
        :return:
        saved_tracks: List[Track]
        """
        r = self.spotipyClient.current_user_saved_tracks(limit=LIMIT)
        saved_tracks = []
        for idx, item in enumerate(r['items']):
            track = self._create_track(item)
            saved_tracks.append(track)
        return saved_tracks

    def current_user_saved_album_tracks(self) -> List[Track]:
        """
        Return all the tracks of the user's last 50 saved albums.
        :return:
        saved_tracks: List[Track]
        """
        r = self.spotipyClient.current_user_saved_albums(limit=LIMIT)
        saved_tracks = []
        for idx, album in enumerate(r['items']):
            detailed_track_json = [self.spotipyClient.track(i['uri']) for i in album['album']['tracks']['items']]
            album_tracks = [self._create_track({'track': track_resp}) for track_resp in detailed_track_json]
            saved_tracks = [*saved_tracks, *album_tracks]
        return saved_tracks

    def get_audio_features(self, tracks) -> Dict:
        # TODO: extract other features
        """
        Returns the audio analysis of each track (as given by Spotify)
        :param tracks:
        tracks: List[Track]
        :return:
        Dict
        """
        track_uris = [track.track_uri for track in tracks]
        r = []
        for chunk in chunks(track_uris, LIMIT):
            r = [*r, *self.spotipyClient.audio_features(tracks=chunk)]
        saved_tracks_audio_analysis = dict(zip(track_uris, r))
        return saved_tracks_audio_analysis

    def make_playlist(self, name, tracks):
        p_response = self._create_playlist(name)
        # need the id (rather than name) to add songs later
        playlist_id = p_response['id']
        return self._add_songs_to_playlist(playlist_id=playlist_id, items=tracks)

    def _create_playlist(self, name):
        return self.spotipyClient.user_playlist_create(user='',
                                                       name=name,
                                                       public=True,
                                                       collaborative=False,
                                                       description='Testing')

    def _add_songs_to_playlist(self, playlist_id, items):
        return self.spotipyClient.playlist_add_items(playlist_id, items, position=None)

    @staticmethod
    def _create_track(item):
        track = Track(track_id=item['track']['id'],
                      track_uri=item['track']['uri'],
                      track_name=item['track']['name'],
                      artist_id=item['track']['artists'][0]['id'],
                      artist_uri=item['track']['artists'][0]['uri'],
                      artist_name=item['track']['artists'][0]['name'],
                      popularity=item['track']['popularity'],
                      duration_ms=item['track']['duration_ms'])
        return track
