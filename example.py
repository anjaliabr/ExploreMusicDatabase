# import packages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column, HorizontalSeparator, In, VSeperator
from PIL import Image
import cloudscraper
import io
import os

# Searching artist
def search_artist(client):
    """
    Use the Spotify client to search for a song and retriece the list of results
    """
    search_query = sg.popup_get_text('Enter the name of the song you want to search:')
    results = client.search(search_query)
    artists = results['tracks']['items'][0]['artists']
    return [f"{artist['name']} - {artist['id']}" for artist in artists]

# Display the features
def display_albums(client, artist_id):
    """
    Use the Spotify client to retrieve the album names of the artist
    """
    info = {}
    albums = client.artist_albums(artist_id)
    artistInfo = client.artist(artist_id)

    info['Artist_Name'] = artistInfo['name']
    info['Artist_ID'] = artist_id
    info['Artist_Img'] = artistInfo['images'][2]['url']

    album_list= [f"{album['name']} - {album['id']} - {album['total_tracks']}" for album in albums['items']]
    
    jpg_data = (
        cloudscraper.create_scraper(
            browser={"browser": "firefox", "platform": "windows", "mobile": False}
        )
        .get(info['Artist_Img'])
        .content
    )
    
    pil_image = Image.open(io.BytesIO(jpg_data))
    png_bio = io.BytesIO()
    pil_image.save(png_bio, format="PNG")
    png_data = png_bio.getvalue()
    
    layout_l =[
        [sg.Text('Artist Name:'), sg.Text(artistInfo['name'])],
        [sg.Text('Followers:'), sg.Text(artistInfo['followers']['total'])],
    ]
    layout_r = [
        [sg.Image(png_data)]
    ]

    layout = [
        [sg.Text('Albums')],
        [sg.Column(layout_l, key='-COL1-', justification='left'), sg.Column(layout_r, key='-COL2-', justification='right')],
        [sg.Listbox(album_list, key='album_list', size=(50,len(album_list)), select_mode='single',bind_return_key=True)],
        [sg.Button('OK'), sg.Cancel()]
    ]

    window = sg.Window('Artist GUI', layout)
    while True:
        event, values = window.Read()
        if event in (None, 'Cancel'):
            break
        if event == 'OK':
            display_tracks(client, values['album_list'][0].split(' - ')[1], info)

def display_tracks(client, album_id, info):
    tracks = client.album_tracks(album_id)
    track_list = [f"{track['track_number']} - {track['name']} - {track['id']}" for track in tracks['items']]
    
    layout = [
        [sg.Listbox(track_list, key='track_list', size=(50,len(track_list)), select_mode='single',bind_return_key=True)],
        [sg.Button('OK'), sg.Cancel()]
    ]

    window = sg.Window('Album GUI', layout)
    while True:
        event, values = window.Read()
        if event in (None, 'Cancel'):
            break
        if event == 'OK':
            final_display(client, values['track_list'][0].split(' - ')[2])

def final_display(client, track_id):
    print(track_id)
    info = client.track(track_id)
    print(len(info['artists']))
    artist = info['artists']
    artistName = []
    for i in range(len(info['artists'])):
        artistName.append(artist[i]['name'])

    sg.popup_scrolled(
        f"Track No.: {info['track_number']} \n"
        f"Track Name: {info['name']}\n"
        f"Track Duration: {info['duration_ms']}\n"
        f"Track URL: {info['uri']}\n"
        f"Album Name: {info['album']['name']} \n"
        f"Album Release Year: {info['album']['release_date']} \n"
        f"Album Type: {info['album']['album_type']}\n"
        f"Artist Name: {artistName} \n"
    )


# Main code
spotipy_cred = SpotifyClientCredentials(client_id="0c9398592c364794a462c4b7947126ea", client_secret="4b9755b57e1949968f3fc052651f25f2")
client = spotipy.Spotify(client_credentials_manager=spotipy_cred)

sg.set_options(font=('Arial', 14))

artist_list = []
layout = [
    [sg.Button('Search', key='search')],
    [sg.Listbox(artist_list, key='artist_list', size=(40,10))],
    [sg.Button('OK'), sg.Button('Cancel')]
]

window = sg.Window('Spotify GUI', layout)
while True:
    event, values = window.Read()
    if event in (None, 'Cancel'):
        break
    elif event == 'search':
        artist_list = search_artist(client)
        print(artist_list)
        window['artist_list'].update(artist_list)
    elif event == 'OK':
        display_albums(client, values['artist_list'][0].split(' - ')[1])

window.close()

