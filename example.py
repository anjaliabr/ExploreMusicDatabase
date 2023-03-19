# import packages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column, HorizontalSeparator, In, VSeperator
import spotipy.util as util
import query as prop
import extra as ex
import json

info_artist = {}
info_album = {}
info_tracks = {}

# Display the features
def display_artist(client, artist_id):
    """
    Use the Spotify client to retrieve the album names of the artist
    """

    artistInfo = prop.search_artist(client, artist_id)
    albums = prop.search_albumbyartist(client, artist_id)

    album_list= [f"{album['name']} - {album['id']} - {album['total_tracks']}" for album in albums['items']]
    
    png_data = ex.imageExtract(artistInfo)
    
    layout_l =[
        [sg.Text('Artist Name:'), sg.Text(artistInfo['name'])],
        [sg.Text('Followers:'), sg.Text(artistInfo['followers']['total'])],
    ]
    layout_r = [
        [sg.Image(png_data)]
    ]

    layout = [
        [sg.Column(layout_r, key='-COL1-', justification='left'), sg.Column(layout_l, key='-COL1-', justification='left')],
        [sg.Text('Albums')],
        [sg.Listbox(album_list, key='album_list', size=(50,len(album_list)), select_mode='single',bind_return_key=True)],
        [sg.Button('OK'), sg.Cancel()]
    ]

    window = sg.Window('Artist GUI', layout)
    while True:
        event, values = window.Read()
        if event in (None, 'Cancel'):
            break
        if event == 'OK':
            display_albums(client, values['album_list'][0].split(' - ')[1])

    info_artist = {
        "id": artistInfo["id"],
        "images": artistInfo["images"][2]["url"],
        "name": artistInfo["name"]
    }

def display_albums(client, album_id):


    with open('./spotifyAPI/albumArtist.json') as f:
        album_dict = json.loads(f.read())
        albums = album_dict["items"]
        for i in range(len(albums)):
            if albums[i]["id"] == album_id:
                info_album = {
                    "id": album_id,
                    "artist": albums[i]["artists"],
                    "album": albums[i]["name"],
                    "images": albums[i]['images'][2]["url"],
                    "year": albums[i]["release_date"][0:4]
                }
    
    tracks = prop.search_tracks(client, album_id)
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


# Info for client_id and client_secret
clientId = "0c9398592c364794a462c4b7947126ea"
secret = "4b9755b57e1949968f3fc052651f25f2"

# Creating credentials
spotipy_cred = SpotifyClientCredentials(client_id=clientId, client_secret=secret)
client = spotipy.Spotify(client_credentials_manager=spotipy_cred)

# Setting the font for the window
sg.set_options(font=('Arial', 14))

artist_list = []

# Creating the layout for the main window
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
        artist_list = prop.search_id(client)
        window['artist_list'].update(artist_list)
        print(artist_list)
    elif event == 'OK':
        display_artist(client, values['artist_list'][0].split(' - ')[1])

window.close()
