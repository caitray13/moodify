import random
import logging


class Moodify:
    """Personalization logic."""
    def __init__(self):
        return

    def filter_tracks_for_mood(self, saved_tracks_audio_analysis,
                               max_valence, min_valence, num_tracks):
        filtered_tracks = []
        for track in saved_tracks_audio_analysis.keys():
            valence = float(saved_tracks_audio_analysis[track]['valence'])
            if (valence >= float(min_valence)) & (valence <= float(max_valence)):
                filtered_tracks.append(track)
        return random.sample(filtered_tracks, min(int(num_tracks), len(filtered_tracks)))
