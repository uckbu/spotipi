import sys
import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Initialize display
epd = epd7in5_V2.EPD()
epd.init()

# Spotify auth
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='6f46637d9d214a998c0e859d3047ddab',
    client_secret='bf0ff2b63eb64f73acbd1ca3a1188c17',
    redirect_uri='http://localhost:8888',
    scope='user-read-currently-playing'))

def get_current_track():
    current = sp.currently_playing()
    if current and current['is_playing']:
        return f"{current['item']['name']}\nby {current['item']['artists'][0]['name']}"
    return "No track playing"

def update_display():
    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
    
    track_info = get_current_track()
    draw.text((50, 200), track_info, font=font, fill=0)
    
    epd.display(epd.getbuffer(image))
    epd.sleep()

while True:
    update_display()
    time.sleep(30)  # Update every 30 seconds