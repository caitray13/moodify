import os
from typing import Dict

from flask import Flask, request, render_template
from spotify import SpotifyService

from record_collection import RecordCollection


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
    saved_tracks = {'results': recordCollection.get_tracks()}
    return saved_tracks


@app.route("/audioanalysis")
def audio_analysis():
    saved_tracks = recordCollection.get_tracks()
    audio_analysis = {'results': spotifyService.get_audio_analysis(saved_tracks)}
    return audio_analysis


# @app.route("/createplaylist")
# def create_mood_playlist():
#     name = request.args.get('name')
#     max_valence = request.args.get('max_valence')
#     min_valence = request.args.get('min_valence')
#     num_tracks = request.args.get('num_tracks')
#     return spotifyService.create_playlist(name, max_valence, min_valence, num_tracks)


if __name__ == '__main__':
    spotifyService = SpotifyService(
        scope='user-read-recently-played user-library-read playlist-modify-public')
    recordCollection = RecordCollection(spotifyService)
    app.run(host=HOST, port=PORT)
