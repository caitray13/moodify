import os
from typing import Dict

from flask import Flask, request, render_template

from record_collection import RecordCollection
from selector import Selector
from spotify import SpotifyService


app = Flask(__name__)

PORT = int(os.getenv('PORT', 8080))
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


@app.route("/createplaylist")
def create_moody_playlist():
    playlist_name = request.args.get('playlist_name')
    max_valence = request.args.get('max_valence')
    min_valence = request.args.get('min_valence')
    num_tracks = request.args.get('num_tracks')
    return selector.create_moody_playlist(playlist_name,
                                          max_valence,
                                          min_valence,
                                          num_tracks)


if __name__ == '__main__':
    spotifyService = SpotifyService(
        scope='user-read-recently-played user-library-read playlist-modify-public')
    recordCollection = RecordCollection(spotifyService)
    selector = Selector(spotifyService, recordCollection)
    app.run(host=HOST, port=PORT)
