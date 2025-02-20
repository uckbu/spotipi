import time
import spotipy
import requests
from io import BytesIO
from spotipy.oauth2 import SpotifyOAuth
from waveshare_epd import epd7in5_V2  # Adjusted for the new e-ink model
from PIL import Image, ImageDraw, ImageFont

# Spotify API credentials
SPOTIPY_CLIENT_ID = "your_client_id"
SPOTIPY_CLIENT_SECRET = "your_client_secret"
SPOTIPY_REDIRECT_URI = "http://localhost:8888/callback"
SCOPE = "user-read-currently-playing"

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

# Initialize e-ink display
epd = epd7in5_V2.EPD()
epd.init()
epd.Clear()

font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 40)

def get_current_song():
    """Fetch currently playing song from Spotify"""
    track_info = sp.currently_playing()
    if track_info and track_info['is_playing']:
        artist = track_info['item']['artists'][0]['name']
        track = track_info['item']['name']
        album_art_url = track_info['item']['album']['images'][0]['url']
        return artist, track, album_art_url
    return None, None, None

def update_display(artist, track, album_art_url):
    """Update e-ink display with album art and text"""
    response = requests.get(album_art_url)
    album_art = Image.open(BytesIO(response.content)).convert('1')
    album_art = album_art.resize((epd.width, epd.height - 50))  # Resize to fit above text

    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)
    image.paste(album_art, (0, 0))
    draw.text((10, epd.height - 40), f"{artist} - {track}", font=font, fill=0)
    
    epd.display(epd.getbuffer(image))

def main():
    while True:
        artist, track, album_art_url = get_current_song()
        if artist and track:
            update_display(artist, track, album_art_url)
        time.sleep(30)  # Update every 30 seconds

if __name__ == "__main__":
    main()
