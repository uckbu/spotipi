import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = '6f46637d9d214a998c0e859d3047ddab'
SPOTIPY_CLIENT_SECRET = 'bf0ff2b63eb64f73acbd1ca3a1188c17'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888'

scope = "user-read-currently-playing"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope))