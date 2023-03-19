import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import PySimpleGUI as sg
from PySimpleGUI.PySimpleGUI import Column, HorizontalSeparator, In, VSeperator
import json
import spotipy.util as util
import extra as ex

# Searching id for artist
def search_id(client):
    """
    Use the Spotify client to search for a song and retriece the list of results
    """
    search_query = sg.popup_get_text('Enter the name of the song you want to search:')
    results = client.search(search_query)
    ex.createJSON(results, "search")
    artists = results['tracks']['items'][0]['artists']
    return [f"{artist['name']} - {artist['id']}" for artist in artists]

def search_albumbyartist(client, artist_id):
    albums = client.artist_albums(artist_id)
    ex.createJSON(albums, "albumArtist")
    return albums

def search_artist(client, artist_id):
    artist = client.artist(artist_id)
    ex.createJSON(artist, "artist")
    return artist

def search_album(client, album_id):
    album = client.albums(album_id)
    ex.createJSON(album, "album")
    return album

def search_tracks(client, album_id):
    tracks = client.album_tracks(album_id)
    ex.createJSON(tracks, "tracks")
    return tracks


