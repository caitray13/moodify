from flask import Flask, request
import json
import os
import spotify

app = Flask(__name__)

PORT = int(os.getenv('PORT', 8080))
HOST = os.getenv('HOST', 'localhost')

@app.route("/")
def home():
    request_data = {'results': spotify.recently_played}
    return request_data


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
