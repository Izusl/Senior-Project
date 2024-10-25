from get_spotify_token import get_token
import requests

#out of script use spotify:track:<id> to search via id in spotify

def get_song_id(song_name, artist=None, limit=1):
    access_token = get_token()
    
    if not access_token:
        print("Failed to retrieve access token.")
        return None

    search_url = 'https://api.spotify.com/v1/search'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    query = f"{song_name} artist:{artist}" if artist else song_name
    params = {
        'q': query,
        'type': 'track',
        'limit': limit
    }
    
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        tracks = response.json().get('tracks', {}).get('items', [])
        
        if tracks:
            song_ids = [track['id'] for track in tracks]
            return song_ids
        else:
            return None
    except requests.exceptions.RequestException as error:
        print('Error fetching song ID:', error)
        return None