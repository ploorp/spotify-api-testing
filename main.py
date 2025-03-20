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
    scope="user-read-currently-playing user-read-recently-played user-read-playback-state"
))


def get_current_song():
    current_song = sp.current_user_playing_track()
    song = current_song['item']['name']
    album = current_song['item']['album']['name']
    artist = current_song['item']['artists'][0]['name']
    track_uri = current_song['item']['uri']
    artist_uri = current_song['item']['artists'][0]['uri']
    artist_img = current_song['item']['artists'][0]['images'][0]['url']
    album_img = current_song['item']['album']['images'][0]['url']
    return f"{song} by {artist}"


def get_recently_played():
    recently_played = sp.current_user_recently_played(limit=10)
    songs = []
    for song in recently_played['items']:
        track = song['track']['name']
        album = song['track']['album']['name']
        artist = song['track']['artists'][0]['name']
        track_uri = song['track']['uri']
        artist_uri = song['track']['artists'][0]['uri']
        artist_img = song['track']['artists'][0]['images'][0]['url']
        album_img = song['track']['album']['images'][0]['url']
        timestamp = song['played_at']
        songs.append([timestamp, track, album, artist, track_uri, artist_uri, artist_img, album_img])
    return songs


def get_last_played():
    last_played = sp.current_user_recently_played(limit=1)
    song = last_played['items'][0]['track']['name']
    album = last_played['items'][0]['track']['album']['name']
    artist = last_played['items'][0]['track']['artists'][0]['name']
    track_uri = last_played['items'][0]['track']['uri']
    artist_uri = last_played['items'][0]['track']['artists'][0]['uri']
    artist_img = last_played['items'][0]['track']['artists'][0]['images'][0]['url']
    album_img = last_played['items'][0]['track']['album']['images'][0]['url']
    timestamp = last_played['items'][0]['played_at']

    time_ago = convert_timestamp_to_time_ago(timestamp)

    return f"{song} by {artist} {time_ago}"


def convert_timestamp_to_time_ago(timestamp):
    played_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    now = datetime.now(timezone.utc)
    time_diff = now - played_time

    hours, remainder = divmod(time_diff.total_seconds(), 3600)
    minutes = remainder // 60

    return f"{int(hours)}h {int(minutes)}m ago" if hours > 0 else f"{int(minutes)}m ago"


def convert_milli_to_time_ago(timestamp):
    played_time = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    time_diff = now - played_time

    hours, remainder = divmod(time_diff.total_seconds(), 3600)
    minutes = remainder // 60

    return f"{int(hours)}h {int(minutes)}m ago" if hours > 0 else f"{int(minutes)}m ago"


def search_song(song_name):
    results = sp.search(q=song_name, type='track')
    return results['tracks']['items']


def main():
    playback = sp.current_playback()

    if playback and playback['currently_playing_type'] == 'track':
        if playback['is_playing']:
            print('currently playing ' + get_current_song())
        else:
            print(f'last played {get_current_song()} {convert_milli_to_time_ago(playback['timestamp'])} (paused)')
    else:
        print(f'last played {get_last_played()}')

main()