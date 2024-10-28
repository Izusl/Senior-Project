import spotipy
from spotipy.exceptions import SpotifyException
import token_cc as tc

# Get the authorization api token
access_token = tc.token_cc()
if not access_token:
    print("Failed to retrieve access token.")
sp = spotipy.Spotify(auth=access_token)

def get_basic_info(track_id):
    try:
        track = sp.track(track_id)
        basic_info = {
            'name': track['name'],
            'popularity': track['popularity'],
            'duration_ms': track['duration_ms'],
            'explicit': track['explicit'],
            'track_number': track['track_number']
        }
        return basic_info
    except SpotifyException as e:
        print("Error retrieving basic info:", e)
        return []

def get_album_details(track_id):
    try:
        track = sp.track(track_id)
        album = track['album']
        album_details = {
            'album_name': album['name'],
            'release_date': album['release_date'],
            'total_tracks': album['total_tracks'],
            'album_cover_url': album['images'][0]['url'] if album['images'] else None
        }
        return album_details
    except SpotifyException as e:
        print("Error retrieving album details:", e)
        return []

def get_artist_details(track_id):
    try:
        track = sp.track(track_id)
        artist = track['artists'][0]
        artist_details = {
            'artist_name': artist['name'],
            'artist_id': artist['id'],
            'spotify_url': artist['external_urls']['spotify']
        }
        return artist_details
    except SpotifyException as e:
        print("Error retrieving artist details:", e)
        return []

def get_audio_features(track_id):
    try:
        audio_features = sp.audio_features(track_id)[0]
        if audio_features:
            features = {
                'acousticness': audio_features['acousticness'],
                'danceability': audio_features['danceability'],
                'energy': audio_features['energy'],
                'instrumentalness': audio_features['instrumentalness'],
                'liveness': audio_features['liveness'],
                'loudness': audio_features['loudness'],
                'speechiness': audio_features['speechiness'],
                'tempo': audio_features['tempo'],
                'valence': audio_features['valence']
            }
            return features
        return []
    except SpotifyException as e:
        print("Error retrieving audio features:", e)
        return []