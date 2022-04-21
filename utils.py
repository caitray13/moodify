import os
import re

import lyricsgenius as lg
import numpy as np
import pandas as pd
import spacy

GENIUS_ACCESS_TOKEN = os.environ.get('GENIUS_ACCESS_TOKEN')
genius = lg.Genius(GENIUS_ACCESS_TOKEN,
                   skip_non_songs=True, 
                   excluded_terms=["(Remix)", "(Live)"], 
                   remove_section_headers=True)

sp = spacy.load('en_core_web_sm')
STOPWORDS = sp.Defaults.stop_words


def get_top_n_similar_tracks(track_names, artists, similarity_matrix, track_name, artist, num):
    track_artist_idx = dict((y,x) for x,y in dict(enumerate(zip(track_names, artists))).items())
    idx = track_artist_idx[(track_name, artist)]
    similar_idx = np.argsort(similarity_matrix[idx])[::-1][1:num+1]
    return [(track_names[i], artists[i]) for i in similar_idx]


def clean_lyrics(lyrics):
    lyrics = lyrics.lower().replace("\n", " ")
    lyrics = lyrics.replace("|", "")
    lyrics = lyrics.replace("\t", "")
    pattern = re.compile('[0-9]*?Embed')
    lyrics = pattern.sub("", lyrics)
    pattern = re.compile('\xa0\xa0\xa0')
    lyrics = pattern.sub("", lyrics)
    doc = sp(lyrics)
    tokens = [token.lemma_ for token in doc if not token.text in STOPWORDS and not token.is_punct]
    # remove some of the tokens
    tokens = [token for token in tokens if token!=" " and token!='lyric']
    return tokens


def get_song_lyrics(title, artist):
    # lyricsgenius has some random timeouts
    while True:
        try:
            song = genius.search_song(title=title, artist=artist)
            break
        except:
            pass
    # song may not be found in lyricsgenius
    if song == None:
        return []
    else:
        cleaned_lyrics = clean_lyrics(song.lyrics)
        return cleaned_lyrics


def build_lyrics_df(track_names, artists):
    lyrics_df = pd.DataFrame(data=zip(track_names, artists), columns=['track_name', 'artist'])
    lyrics_df['lyrics'] = lyrics_df.apply(lambda x: get_song_lyrics(x.track_name, x.artist), axis=1)
    return lyrics_df


def get_top_n_topic_words(lda_model, vocab, num):
    topic_dist = lda_model.components_
    
    for i, dist in enumerate(topic_dist):
        topic_words = np.array(vocab)[np.argsort(dist)]
        top_topic_words = topic_words[:-num:-1]
        print(f'Topic {i+1}: {top_topic_words}')
    
    
    