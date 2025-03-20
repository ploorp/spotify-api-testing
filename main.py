import os
from datetime import datetime, timezone
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
    scope="user-read-currently-playing, user-read-recently-played",
))


def get_current_song():
    current_song = sp.current_user_playing_track()
    if current_song and current_song['is_playing'] and current_song['currently_playing_type'] == 'track':
        song = current_song['item']['name']
        album = current_song['item']['album']['name']
        artist = current_song['item']['artists'][0]['name']
        return f"currently playing {song} by {artist}"
    return "no song found"


def get_recently_played():
    recently_played = sp.current_user_recently_played(limit=10)
    songs = []
    for song in recently_played['items']:
        track = song['track']['name']
        album = song['track']['album']['name']
        artist = song['track']['artists'][0]['name']
        track_uri = song['track']['uri']
        artist_uri = song['track']['artists'][0]['uri']
        timestamp = song['played_at']
        songs.append([timestamp, track, album, artist, track_uri, artist_uri])
    return songs


def get_last_played():
    last_played = sp.current_user_recently_played(limit=1)
    song = last_played['items'][0]['track']['name']
    album = last_played['items'][0]['track']['album']['name']
    artist = last_played['items'][0]['track']['artists'][0]['name']
    track_uri = last_played['items'][0]['track']['uri']
    artist_uri = last_played['items'][0]['track']['artists'][0]['uri']
    timestamp = last_played['items'][0]['played_at']

    time_ago = convert_timestamp_to_time_ago(timestamp)

    return f"last played {song} by {artist} {time_ago}"


def convert_timestamp_to_time_ago(timestamp):
    played_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    time_diff = now - played_time

    hours, remainder = divmod(time_diff.total_seconds(), 3600)
    minutes = remainder // 60

    return f"{int(hours)}h {int(minutes)}m ago" if hours > 0 else f"{int(minutes)}m ago"


def main():
    if sp.current_playback()['is_playing']:
        print(get_current_song())
    else:
        print(get_last_played())

main()