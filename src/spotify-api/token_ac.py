import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = '67dc3d054c744ea1a0e7f532cf53c4ee'
client_secret = '25823d4675db4cb0a5ea6f1c6bbea956'
redirect_uri = 'http://localhost:8888/callback'

def token_ac():
    scope = 'user-read-playback-state user-read-currently-playing user-read-private'

    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope)

    print("Getting access token...")
    access_token = sp_oauth.get_access_token(as_dict=False)
    print("Access token retrieval complete.")

    if not access_token:
        print("Failed to retrieve access token.")
    else:
        print(f"Access Token: {access_token}")
        return access_token

if __name__ == '__main__':
    token_ac()