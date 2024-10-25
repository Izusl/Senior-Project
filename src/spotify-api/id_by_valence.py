from get_spotify_token import get_token
import spotipy

def get_songs_by_emotion(emotion, limit=3):
    access_token = get_token()
    
    if not access_token:
        print("Failed to retrieve access token.")
        return []
    
    sp = spotipy.Spotify(auth=access_token)

    # Define valence thresholds for emotions
    emotion_thresholds = {
        "happy": (0.5, 1.0),
        "sad": (0.0, 0.5)
    }
    
    if emotion not in emotion_thresholds:
        print("Emotion not supported.")
        return []
    
    min_valence, max_valence = emotion_thresholds[emotion]

    # Search for tracks
    results = sp.search(q='a', type='track', limit=50)
    song_ids = []
    
    for track in results['tracks']['items']:
        track_id = track['id']
        features = sp.audio_features(track_id)[0]
        
        if features and min_valence <= features['valence'] <= max_valence:
            song_ids.append(track_id)
    
    return song_ids[:limit]