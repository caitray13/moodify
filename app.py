import logging
import os
from typing import Dict

from flask import Flask, request, render_template

from record_collection import RecordCollection
from selecta import Selecta
from spotify import SpotifyService

logging.basicConfig(level = logging.INFO)


app = Flask(__name__)

PORT = int(os.getenv('PORT', 5000))
HOST = os.getenv('HOST', 'localhost')


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/recent")
def recent():
    request_data = {'results': spotifyService.current_user_recently_played()}
    return request_data


@app.route("/savedtracks")
def saved_tracks() -> Dict:
    tracks = {'results': recordCollection.get_tracks()}
    return tracks


@app.route("/audioanalysis")
def audio_analysis():
    tracks = recordCollection.get_tracks()
    audio_analysis = {'results': spotifyService.get_audio_analysis(tracks)}
    return audio_analysis


@app.route("/createplaylist/<type>")
def create_playlist(type):
    match type:
        case "moody":
            return create_moody_playlist()
        case "lyrics":
            return create_lyrics_playlist()
        case _:
            return "That's not a type of playlist we can do."


def create_moody_playlist():
    playlist_name = request.args.get('playlist_name')
    max_valence = request.args.get('max_valence')
    min_valence = request.args.get('min_valence')
    num_tracks = request.args.get('num_tracks', type=int)
    return selector.create_moody_playlist(playlist_name,
                                          max_valence,
                                          min_valence,
                                          num_tracks)


def create_lyrics_playlist():
    track_name = request.args.get('track_name')
    artist_name = request.args.get('artist_name')
    num_tracks = request.args.get('num_tracks', type=int)
    return selector.create_similar_lyrics_playlist(spotify_id, track_name, artist_name, num_tracks)    


if __name__ == '__main__':
    logging.info('Connecting to Spotify...')
    spotifyService = SpotifyService(
        scope='user-read-recently-played user-library-read playlist-modify-public')
    spotify_id = spotifyService.spotipyClient.current_user()["id"]
    logging.info(f'Spinning up record collection for {spotify_id}...')
    recordCollection = RecordCollection()
    recordCollection.build_collection(spotifyService, spotify_id) 
    selector = Selecta(spotifyService, recordCollection)
    logging.info('Rude boi selecta is ready for requests!')
    app.run(host='0.0.0.0', port=PORT)