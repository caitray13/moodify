import spotipy
from spotipy.oauth2 import SpotifyOAuth

from typing import Dict, List, Any


class SpotifyService():
    def __init__(self, scope) -> None:
        self.scope = scope
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope='user-read-recently-played'))

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
    

    
    
    """def get_top_artists(self, limit=20, time_range='medium_term')-> Dict[Any, List[Any]]:
        Get top artists and their genres.

        Parameters
        ------------
        limit: int
            number of artists to return.
        
        Returns
        ------------
        dict str -> list(str)
            dict with artists as the keys and list of genres as values.
        
        scope = 'user-top-read'
        r = self.spotify.current_user_top_artists(limit=limit, time_range=time_range)
        return r"""
