import requests
import base64

client_id = '67dc3d054c744ea1a0e7f532cf53c4ee'
client_secret = '25823d4675db4cb0a5ea6f1c6bbea956'

def get_token():
    token_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {auth_header}'
    }
    
    data = {
        'grant_type': 'client_credentials'
    }
    
    try:
        response = requests.post(token_url, headers=headers, data=data)
        response.raise_for_status()
        access_token = response.json().get('access_token')
        return access_token
    except requests.exceptions.RequestException as error:
        print('Error fetching token:', error)

if __name__ == '__main__':
    get_token()