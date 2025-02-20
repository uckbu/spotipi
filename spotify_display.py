import sys
import time
from PIL import Image, ImageDraw, ImageFont
from waveshare_epd import epd7in5_V2
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import requests
from io import BytesIO

# Spotify credentials
SPOTIPY_CLIENT_ID = ''
SPOTIPY_CLIENT_SECRET = ''
SPOTIPY_REDIRECT_URI = ''
SCOPE = 'user-read-currently-playing'
CACHE_PATH = os.path.join(os.path.expanduser('~'), '.cache-spotify')

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
            track_name = current['item']['name']
            artist_name = current['item']['artists'][0]['name']
            album_cover_url = current['item']['album']['images'][0]['url']
            duration_ms = current['item']['duration_ms']
            progress_ms = current['progress_ms']
            time_remaining = (duration_ms - progress_ms) / 1000
            return track_name, artist_name, album_cover_url, time_remaining
        return None, None, None, 10  # Default wait time if no track is playing
    except Exception as e:
        print(f"Error getting current track: {str(e)}")
        return None, None, None, 10

def fetch_album_cover(url):
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error fetching album cover: {str(e)}")
        return None

def update_display(track_name, artist_name, album_cover):
    try:
        epd = epd7in5_V2.EPD()
        epd.init()
        
        image = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(image)
        
        # Load fonts
        font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 32)
        font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
        
        # Resize album cover to fit most of the display
        cover_resized = album_cover.resize((epd.width, int(epd.height * 0.8)))
        image.paste(cover_resized, (0, 0))
        
        # Draw song info in bottom left corner
        draw.text((10, epd.height - 60), track_name, font=font_large, fill=0)
        draw.text((10, epd.height - 30), artist_name, font=font_small, fill=0)
        
        epd.display(epd.getbuffer(image))
        epd.sleep()
    except Exception as e:
        print(f"Error updating display: {str(e)}")

def main():
    last_song = None
    
    try:
        print("Starting Spotify Display...")
        print("Press CTRL+C to stop")
        
        while True:
            track_name, artist_name, album_cover_url, wait_time = get_current_track()
            wait_time = min(wait_time, 60)  # Limit wait time to 60 seconds
            if track_name and track_name != last_song:
                album_cover = fetch_album_cover(album_cover_url) if album_cover_url else None
                if album_cover:
                    update_display(track_name, artist_name, album_cover)
                last_song = track_name
            
            time.sleep(wait_time)  # Only update after song duration
    
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
