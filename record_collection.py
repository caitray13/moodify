from dataclasses import dataclass, asdict, field
from typing import Dict, List, Optional

import boto3

from track import Track
import utils

DYNAMODB = boto3.resource('dynamodb')
TABLE = DYNAMODB.Table('SpotificationLyrics')


def already_user(spotify_id):
    response = TABLE.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('spotify_id').eq(spotify_id)
    )
    if response['Count'] > 0:
        return True
    else:
        return False


@dataclass
class RecordCollection:
    tracks: Optional[List[Track]] = field(default_factory=list)
 
    def __build_new_collection(self, spotifyService):
        self.tracks = [*spotifyService.current_user_saved_tracks(),
                       *spotifyService.current_user_saved_album_tracks(),
                       *spotifyService.current_user_recently_played()]
        for track in self.tracks:
            track.lyrics = utils.get_song_lyrics(track.track_name, track.artist_name)

    def __build_existing_collection(self, spotify_id):
        response = TABLE.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('spotify_id').eq(spotify_id),
            Limit=10  # TODO: remove this
        )
        items = response["Items"]
        tracks = []
        for item in items:
            track = Track(track_uri=item['track_uri'],
                          track_name=item['track_name'],
                          artist_name=item['artist'],
                          lyrics=item['lyrics'])
            tracks.append(track)
        self.tracks = tracks

    def build_collection(self, spotifyService, spotify_id):
        if already_user(spotify_id)==True:
            self.__build_existing_collection(spotify_id)
        else:
            self.__build_new_collection(spotifyService)

    def get_tracks(self) -> List[Dict]:
        return [asdict(track) for track in self.tracks]
    
    def record_in_collection(self, track_name, artist_name):
        found = False
        for track in self.tracks:
            if track.track_name == track_name and track.artist_name == artist_name:
                found=True
                break
            else:
                continue
        return found

    def __str__(self):
        return f"Record collection made up of {len(self.tracks)} songs."