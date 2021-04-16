import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-recently-played"

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = spotify.current_user_recently_played()
recently_played = []
for idx, item in enumerate(results['items']):
    track = item['track']
    recently_played_song = {}
    recently_played_song['artists'] = track['artists'][0]['name']
    recently_played_song['name'] = track['name']
    recently_played.append(recently_played_song)
    print(idx, recently_played_song['artists'], " – ", recently_played_song['name'])
