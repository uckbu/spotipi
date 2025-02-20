import sys
import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Spotify credentials
SPOTIPY_CLIENT_ID = '6f46637d9d214a998c0e859d3047ddab'
SPOTIPY_CLIENT_SECRET = 'bf0ff2b63eb64f73acbd1ca3a1188c17'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888'
SCOPE = 'user-read-currently-playing'
CACHE_PATH = os.path.join(os.path.expanduser('~'), '.cache-spotify')

# Initialize Spotify client using the same cache path as auth script
auth_manager = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE_PATH
)

sp = spotipy.Spotify(auth_manager=auth_manager)

def get_current_track():
    try:
        current = sp.currently_playing()
        if current and current['is_playing']:
            return f"{current['item']['name']}\nby {current['item']['artists'][0]['name']}"
        return "No track playing"
    except Exception as e:
        print(f"Error getting current track: {str(e)}")
        return "Error getting track info"

def update_display():
    try:
        # Reinitialize the display before each update
        epd = epd7in5_V2.EPD()
        epd.init()
        
        # Create the image
        image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
        
        track_info = get_current_track()
        draw.text((50, 200), track_info, font=font, fill=0)
        
        # Display and sleep
        epd.display(epd.getbuffer(image))
        epd.sleep()
        
    except Exception as e:
        print(f"Error updating display: {str(e)}")

def main():
    try:
        print("Starting Spotify Display...")
        print("Press CTRL+C to stop")
        
        while True:
            update_display()
            time.sleep(30)  # Update every 30 seconds
            
    except KeyboardInterrupt:
        print("\nProgram stopped by user")
        try:
            epd = epd7in5_V2.EPD()
            epd.init()
            epd.Clear()
            epd.sleep()
        except:
            pass
        
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        try:
            epd = epd7in5_V2.EPD()
            epd.init()
            epd.Clear()
            epd.sleep()
        except:
            pass

if __name__ == "__main__":
    main()