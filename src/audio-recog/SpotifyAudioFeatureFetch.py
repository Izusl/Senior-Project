import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import threading
import sys
sys.path.insert(0, '../spotify-api')
import get_token as gt

# Set up your credentials and redirect URI
redirect_url = 'http://localhost:8888/callback'
auth = gt.get_token()

# Scopes required to access current playback and audio features
SCOPE = 'user-read-playback-state user-read-currently-playing user-read-private'

class SpotifyTracker:
    def __init__(self):
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=gt.client_id,
                                                            client_secret=gt.client_secret,
                                                            redirect_uri=redirect_url,
                                                            scope=SCOPE))
        self.current_track_id = None  # Track ID for the current song
        self.stop_thread = False  # Flag to stop the checking thread

    def get_current_track_audio_features(self):
        try:
            # Get the currently playing track
            current_playback = self.sp.current_playback()

            # List of checks to perform
            checks = [
                (current_playback, "No track is currently playing."),
                (current_playback.get('is_playing'), "Current playback is not playing."),
                (current_playback.get('item'), "No track item found in current playback."),
                (current_playback.get('item').get('id'), "No track ID found.")
            ]

            # Execute checks
            for condition, message in checks:
                if not condition:
                    print(message)
                    return None

            # Get track ID and audio features
            track_id = current_playback['item']['id']
            if track_id == self.current_track_id:
                return None

            self.current_track_id = track_id
            audio_features = self.sp.audio_features(track_id)

            if not audio_features or not audio_features[0]:
                print("Audio features request returned None or no features found.")
                return None
            return audio_features[0]

        except Exception as e:
            print(f"Error retrieving audio features: {e}")
            return None


    def track_audio_features(self):
        while not self.stop_thread:
            audio_features = self.get_current_track_audio_features()

            if audio_features is not None:
                print("Audio Features of the Current Track:")
                for feature, value in audio_features.items():
                    print(f"{feature.capitalize()}: {value if value is not None else 'N/A'}")

            time.sleep(5)  # Wait before checking again to avoid rate limits

if __name__ == "__main__":
    tracker = SpotifyTracker()  # Create an instance of SpotifyTracker

    # Start the audio features tracking in a separate thread
    thread = threading.Thread(target=tracker.track_audio_features)
    thread.start()

    # Wait for user input to stop the program
    exitInput = input("Press a key to stop...\n")
    tracker.stop_thread = True  # Signal the thread to stop
    thread.join()  # Wait for the thread to finish
    sys.exit(0)
