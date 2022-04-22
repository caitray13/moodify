import numpy as np
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

sp = spacy.load('en_core_web_sm')
STOPWORDS = sp.Defaults.stop_words
N_TOPICS = 5

class LdaModel():
    def __init__(self, recordCollection):
        self.track_uris = [track.track_uri for track in recordCollection.tracks]
        self.track_names = [track.track_name for track in recordCollection.tracks]
        self.artist_names = [track.artist_name for track in recordCollection.tracks]
        self.lyrics_corpus = self.build_lyrics_corpus(recordCollection.tracks)


    def build_lyrics_corpus(self, tracks):
        lyrics_corpus = []
        for track in tracks:
            track_lyrics = track.lyrics
            lyrics_corpus.append(track_lyrics)
        return lyrics_corpus
    
    
    def vectorize(self, corpus):
        cv = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)
        return cv.fit_transform(corpus)


    def build_model(self, corpus_transformed):
        lda_model = LatentDirichletAllocation(n_components=N_TOPICS, max_iter=20)
        topics = lda_model.fit_transform(corpus_transformed)
        return cosine_similarity(topics)


    def get_top_n_similar_tracks(self, similarity_matrix, track_name, artist_name, num):
        track_artist_idx = dict((y,x) for x,y in dict(enumerate(zip(self.track_names, self.artist_names))).items())
        idx = track_artist_idx[(track_name, artist_name)]
        similar_idx = np.argsort(similarity_matrix[idx])[::-1][1:num+1]
        print([(self.track_names[i], self.artist_names[i]) for i in similar_idx])
        return 


    def get_recommendations(self, track_name, artist_name, num_tracks):
        corpus_transformed = self.vectorize(self.lyrics_corpus)
        similarity_matrix = self.build_model(corpus_transformed)
        recommendations = self.get_top_n_similar_tracks(similarity_matrix, 
                                                        track_name, 
                                                        artist_name, 
                                                        num_tracks)
        return recommendations
    
    
    