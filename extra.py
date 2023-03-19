import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from PIL import Image
import cloudscraper
import io
import os
import json
import requests

def createJSON(data, name):
    with open(f'./spotifyAPI/{name}.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def imageExtract(data):
    jpg_data = (
        cloudscraper.create_scraper(
            browser={"browser": "firefox", "platform": "windows", "mobile": False}
        )
        .get(data['images'][2]['url'])
        .content
    )
    
    pil_image = Image.open(io.BytesIO(jpg_data))
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()

    return png_data