#import these to use the function
import sys
sys.path.insert(0, '../spotify-api')
from emotions_get_id import get_songs_by_emotion
#---------------------------------------

# example
sad_songs = get_songs_by_emotion("sad", limit=3)
print("Sad Songs:", sad_songs)

happy_songs = get_songs_by_emotion("happy", limit=3)
print("Happy Songs:", happy_songs)