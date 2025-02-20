import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

SPOTIPY_CLIENT_ID = '6f46637d9d214a998c0e859d3047ddab'
SPOTIPY_CLIENT_SECRET = 'bf0ff2b63eb64f73acbd1ca3a1188c17'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888'

scope = "user-read-currently-playing"

# Create SpotifyOAuth object
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    open_browser=False  # Prevent automatic browser opening
))

# Get the token info directly from the auth manager
token_info = sp.auth_manager.get_cached_token()

if token_info is None:
    # If no valid token exists, get a new one
    token_info = sp.auth_manager.get_access_token()

# Format the token info into the desired structure
formatted_token = {
    "access_token": token_info["access_token"],
    "token_type": "Bearer",
    "expires_in": token_info["expires_in"],
    "refresh_token": token_info["refresh_token"],
    "scope": scope,
    "expires_at": token_info["expires_at"]
}

# Save the formatted token info to a JSON file
with open("spotify_token.json", "w") as token_file:
    json.dump(formatted_token, token_file, indent=2)

print("Authentication successful! Token saved to spotify_token.json file.")