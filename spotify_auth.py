import spotipy
import json
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = '6f46637d9d214a998c0e859d3047ddab'
SPOTIPY_CLIENT_SECRET = 'bf0ff2b63eb64f73acbd1ca3a1188c17'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888'

scope = "user-read-currently-playing"

# Create SpotifyOAuth object
sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope,
    cache_path=".cache"
)

# Get the authorization URL
auth_url = sp_oauth.get_authorize_url()
print(f"Please navigate to this URL to authorize the app: {auth_url}")

# Prompt the user to input the redirect URL after authorization
response = input("Enter the URL you were redirected to after authorization: ")

# Extract the authorization code from the redirect URL
code = sp_oauth.parse_response_code(response)

# Get the access token
token_info = sp_oauth.get_access_token(code)

# Save the token info to the cache file in JSON format
with open(".cache", "w") as cache_file:
    json.dump(token_info, cache_file)

print("Authentication successful! Token saved to .cache file.")