from flask import Flask, request
import json
import os
from spotify import SpotifyService

app = Flask(__name__)

PORT = int(os.getenv('PORT', 8080))
HOST = os.getenv('HOST', 'localhost')

@app.route("/")
def home():
    request_data = {'results': spotify.get_recently_played()}
    return request_data

@app.route("/savedtracks")
def saved_tracks():
    saved_tracks = {'results': spotify.get_saved_tracks()}
    return saved_tracks


if __name__ == '__main__':
    spotify = SpotifyService(scope='user-read-recently-played user-library-read')
    app.run(host=HOST, port=PORT)
