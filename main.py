import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id, 
    client_secret=client_secret, 
    scope="user-read-currently-playing"))

def get_current_song():
    current_song = sp.current_user_playing_track()
    if current_song:
        song = current_song['item']['name']
        artist = current_song['item']['artists'][0]['name']
        return f"{song} by {artist}"
    return "no song found"

print(get_current_song())