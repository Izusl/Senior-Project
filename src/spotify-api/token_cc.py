import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = '67dc3d054c744ea1a0e7f532cf53c4ee'
client_secret = '25823d4675db4cb0a5ea6f1c6bbea956'

def token_cc():

    print("Getting access token...")
    client_cred = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    print("Access token retrieval complete.")
    access_token = client_cred.get_access_token(as_dict=False)
    
    if not access_token:
        print("Failed to retrieve access token.")
    else:
        print(f"Access Token: {access_token}")
        return access_token

if __name__ == '__main__':
    token_cc()