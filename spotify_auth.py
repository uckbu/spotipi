import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = '6f46637d9d214a998c0e859d3047ddab'
SPOTIPY_CLIENT_SECRET = 'bf0ff2b63eb64f73acbd1ca3a1188c17'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888'
SCOPE = 'user-read-currently-playing'
CACHE_PATH = '.spotify_token.json'

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE,
        open_browser=False,
        cache_path=CACHE_PATH
    )

# Remove existing cache if it exists
if os.path.exists(CACHE_PATH):
    os.remove(CACHE_PATH)

# Create new auth manager
auth_manager = create_spotify_oauth()

# Get auth url
auth_url = auth_manager.get_authorize_url()
print(f"\nPlease navigate to this URL to authorize the app:\n{auth_url}\n")

# Get the code from redirect URL
response = input("Enter the URL you were redirected to: ")
code = auth_manager.parse_response_code(response)

# Get the access token
token_info = auth_manager.get_access_token(code, as_dict=True, check_cache=False)

# Format token info
formatted_token = {
    "access_token": token_info["access_token"],
    "token_type": "Bearer",
    "expires_in": token_info["expires_in"],
    "refresh_token": token_info["refresh_token"],
    "scope": SCOPE,
    "expires_at": token_info["expires_at"]
}

# Save formatted token
with open('spotify_token.json', 'w') as f:
    json.dump(formatted_token, f, indent=2)

print("\nAuthentication successful! Token saved to spotify_token.json")

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