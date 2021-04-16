import spotipy
from spotipy.oauth2 import SpotifyOAuth

from typing import Dict, List


class SpotifyService():
    def __init__(self, scope) -> None:
        self.scope = scope
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def get_recently_played(self) -> List[Dict]:
        r = self.spotify.current_user_recently_played()
        recently_played = []
        for idx, item in enumerate(r['items']):
            track = item['track']
            recently_played_song = {}
            recently_played_song['artists'] = track['artists'][0]['name']
            recently_played_song['name'] = track['name']
            recently_played.append(recently_played_song)
            print(idx, recently_played_song['artists'],
                  " – ", recently_played_song['name'])
        return recently_played
