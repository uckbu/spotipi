import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''
SCOPE = 'user-read-currently-playing'

# Use consistent cache path
CACHE_PATH = os.path.join(os.path.expanduser('~'), '.cache-spotify')

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        open_browser=False,
        cache_path=CACHE_PATH
    )

# Create new auth manager
auth_manager = create_spotify_oauth()

# Get auth url
auth_url = auth_manager.get_authorize_url()
print(f"\nPlease navigate to this URL to authorize the app:\n{auth_url}\n")

# Get the code from redirect URL
response = input("Enter the URL you were redirected to: ")
code = auth_manager.parse_response_code(response)

# Get the access token
token_info = auth_manager.get_access_token(code, check_cache=False)

print("\nAuthentication successful! Token cached at:", CACHE_PATH)

# Verify the token works
try:
    sp = spotipy.Spotify(auth_manager=auth_manager)
    current_track = sp.currently_playing()
    print("\nToken verification successful!")
    if current_track and current_track['is_playing']:
        print(f"Currently playing: {current_track['item']['name']}")
    else:
        print("No track currently playing")
except Exception as e:
    print(f"\nError verifying token: {str(e)}")
