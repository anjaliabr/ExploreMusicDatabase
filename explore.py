# import packages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#user id= 317ivbyrf4tbgbydnf7mbodwgkdy

cid = '0c9398592c364794a462c4b7947126ea'
secret = '4b9755b57e1949968f3fc052651f25f2'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

# Search "Green Day" in artists and return only the first result
result = sp.search("green day", type='album')
# Display genres associated with the first search result
print(result["albums"]['items'][0]['genres'])

# Create spotify object
name = 'Halsey'
searchArtist = sp.search(name)
for artist in searchArtist['tracks']['items'][0]['artists']:
    print(f"{artist['name']} - {artist['id']}")
#print(f"Artist Name: {searchArtist['artists']['items'][0]['name']}, Artist ID: {searchArtist['artists']['items'][0]['id']}")
artistID = searchArtist['tracks']['items'][0]['artists'][1]['id']
artistAlbum = sp.artist_albums(artistID)

#for album in artistAlbum['items']:
 #   print(f"Album Name: {album['name']}, Album ID: {album['id']}, No. of Tracks: {album['total_tracks']}")

#albumName = artistAlbum['items'][0]['name']
#albumID = artistAlbum['items'][0]['id']
#print(albumID)

#artists = []

#tracks = sp.album_tracks(albumID)
#for track in tracks['items']:
 #   for artist in track['artists']:
  #      artists.append(artist['name'])
   # print(f"Track No: {track['track_number']}, Track Name: {track['name']}, Artists: {artists}")
    #artists = []