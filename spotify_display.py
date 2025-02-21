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
SPOTIPY_CLIENT_ID = '6f46637d9d214a998c0e859d3047ddab'
SPOTIPY_CLIENT_SECRET = 'bf0ff2b63eb64f73acbd1ca3a1188c17'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888'
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

def get_weather():
    try:
        weather_url = "https://api.open-meteo.com/v1/forecast?latitude=YOUR_LAT&longitude=YOUR_LON&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode&timezone=auto"
        response = requests.get(weather_url)
        data = response.json()
        hi_temp_c = data['daily']['temperature_2m_max'][0]
        lo_temp_c = data['daily']['temperature_2m_min'][0]
        hi_temp_f = (hi_temp_c * 9/5) + 32
        lo_temp_f = (lo_temp_c * 9/5) + 32
        precipitation = data['daily']['precipitation_sum'][0]
        weather_code = data['daily']['weathercode'][0]
        weather_icon = fetch_weather_icon(weather_code, precipitation)
        return f"Hi: {hi_temp_f:.1f}°F Lo: {lo_temp_f:.1f}°F Precip: {precipitation}mm", weather_icon
    except Exception as e:
        print(f"Error fetching weather: {str(e)}")
        return "Weather Unavailable", None

def fetch_weather_icon(weather_code, precipitation):
    try:
        weather_icons = {
            0: "icons/sun.png",
            1: "icons/mostly_sunny.png",
            2: "icons/partly_cloudy.png",
            3: "icons/cloudy.png",
            61: "icons/rainy.png",
            71: "icons/snowy.png"
        }
        icon_path = weather_icons.get(weather_code, "icons/unknown.png")
        return Image.open(icon_path)
    except Exception as e:
        print(f"Error fetching weather icon: {str(e)}")
        return None

def update_display(track_name, artist_name, album_cover, weather_info, weather_icon):
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
        
        # Draw weather info and move it left to make space for icon
        draw.text((epd.width - 250, epd.height - 60), weather_info, font=font_small, fill=0)
        if weather_icon:
            image.paste(weather_icon, (epd.width - 80, epd.height - 80))
        
        epd.display(epd.getbuffer(image))
        epd.sleep()
    except Exception as e:
        print(f"Error updating display: {str(e)}")


