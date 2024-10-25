#import these to use the function
import sys
sys.path.insert(0, '../spotify-api')
from get_song_id import get_song_id
#---------------------------------------

# example
song_name = "Imagine"
artist_name = "John Lennon" #optional defaults null
limit = 1 #optional defaults 1 dont do 99999999999 or you may get rate limited

song_ids = get_song_id(song_name, artist_name, limit)
if song_ids:
    print(f"Found song IDs: {song_ids}")
else:
    print("No songs found.")