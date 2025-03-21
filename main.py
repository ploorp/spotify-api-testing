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
    artist = current_song['item']['artists'][0]['name'] # just gets main artist
    track_uri = current_song['item']['uri']
    artist_uri = current_song['item']['artists'][0]['uri']
    #artist_img = sp.artist(artist_uri)['images'][0]['url']
    album_img = current_song['item']['album']['images'][0]['url']
    return [song, album, artist, track_uri, artist_uri, album_img]


def get_recently_played(count):
    recently_played = sp.current_user_recently_played(limit=count)
    songs = []
    for song in recently_played['items']:
        track = song['track']['name']
        album = song['track']['album']['name']
        artist = song['track']['artists'][0]['name'] # just gets main artist
        track_uri = song['track']['uri']
        artist_uri = song['track']['artists'][0]['uri']
        #artist_img = sp.artist(artist_uri)['images'][0]['url']
        album_img = song['track']['album']['images'][0]['url']
        timestamp = song['played_at']
        songs.append([timestamp, track, album, artist, track_uri, artist_uri, album_img])
    return songs


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
        current_song = get_current_song()
        if playback['is_playing']:
            print(f'currently playing {current_song[0]} by {current_song[2]}')
        else:
            time_ago = convert_milli_to_time_ago(playback['timestamp'])
            print(f'last played {current_song[0]} by {current_song[2]} {time_ago} (paused)')
    else:
        last_song = get_recently_played(1)
        time_ago = convert_timestamp_to_time_ago(last_song[0][0])
        print(f'last played {last_song[0][1]} by {last_song[0][3]} {time_ago}')

main()