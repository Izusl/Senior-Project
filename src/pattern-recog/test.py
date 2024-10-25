#import these to use the function
import sys
sys.path.insert(0, '../spotify-api')

import track_attributes as ta
import song_filter as sf
#---------------------------------------

# example

songs = sf.filter_by_valence("sad", 1)
print("Filtered ID's: ", songs)
print("Song found: ", ta.get_basic_info(songs[0])['name'], " by ", ta.get_artist_details(songs[0])['artist_name'])