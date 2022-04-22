import logging

import boto3

from spotify import SpotifyService
from record_collection import RecordCollection
import utils

from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)

DYNAMODB = boto3.resource('dynamodb')
TABLE = DYNAMODB.Table('SpotificationLyrics')

def batch_write(table, table_data):
    try:
        with table.batch_writer(overwrite_by_pkeys=['track_uri']) as bw:
            for i, record in enumerate(table_data):
                bw.put_item(Item=record)
        logger.info(f"Loaded data into table: {table.name}.")
    except ClientError:
        logger.exception("Couldn't load data into table: {table.name}.")
        raise

def format_table_data(recordCollection):
    table_data = []
    
    for track in recordCollection.tracks:
        track_uri = track.track_uri
        track_name = track.track_name
        artist = track.artist_name
        cleaned_lyrics = utils.get_song_lyrics(track_name, artist)
        table_data.append({
            'track_uri': track_uri, 
            'track_name': track_name, 
            'artist': artist, 
            'lyrics': cleaned_lyrics})
    
    return table_data

if __name__ == '__main__':
    spotifyService = SpotifyService(scope='user-read-recently-played')
    recordCollection = RecordCollection(spotifyService = spotifyService)
    logger.info(f"Record collection downloaded.")
    logger.info(f"{str(recordCollection)}")
    formatted_table_data = format_table_data(recordCollection)
    batch_write(TABLE, formatted_table_data)
    
    
    
    
    
    
    



