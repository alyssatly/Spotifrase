import sys
import spotipy
import spotipy.util as util
import json
import requests
from flask_cors import CORS


import random
from flask import Flask
app = Flask(__name__)
CORS(app)

SPOTIPY_CLIENT_ID = '1a4a4b75393745f785181b63c3e3241d'
SPOTIPY_CLIENT_SECRET = 'c29f88cdd9b146bf8e3973c19f6db37a'
SPOTIPY_REDIRECT_URI = "https://www.getpostman.com/oauth2/callback" #"http://local  host:3000" literally don't know which one lmfao

scope = "playlist-modify-public"
username = 'jic8ivr1lzroc34t324vygv1t' #input("Enter username: ")
password = 'HackUCI123!@#'

URL = 'https://accounts.spotify.com/authorize'
PARAMS = { 'client_id': SPOTIPY_CLIENT_ID, 'response_type': 'code', 'redirect_uri': SPOTIPY_REDIRECT_URI }
r = requests.get(url=URL, params=PARAMS)

# user_playlist_create(user, name, public=True, description='')
token = util.prompt_for_user_token(username,scope,client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET,redirect_uri=SPOTIPY_REDIRECT_URI)

sp = spotipy.Spotify(auth=token)

# functions

## Search based off words. Start with small phrases
## and go up until you find the song title with the largest 
## amount of words used. 
@app.route('/getByTitle/<search_str>/<playlist_name>')
def search_title(search_str : str, playlist_name="Your Playlist") -> list: 
    # loop through words in search_str to find matching songs
    songs = []
    last_song = ''
    search_list = search_str.split(" ")
    valid_songs = []

    # current word
    word = 0
    while word < len(search_list) :

        for i in range(word+1, len(search_list)+1):
            # current search string
            current_search = ' '.join(search_list[word:i])

            # search through Spotipy
            results = sp.search(q=current_search, type='track')

            # if there are results, then iterate through them to find match
            if len(results['tracks']['items']) > 0:
                # number of results to go through
                if len(results['tracks']['items']) > 10:
                    search_count = 10
                else:
                    search_count = len(results['tracks']['items'])
                
                # find the longest valid search that matches exactly
                for k in range(search_count):
                    current_song = results['tracks']['items'][k]
                    #print("current_song: ", current_song)
                    #print("current_search.lower(): ", current_search.lower())
                    #print("current_song['name'].lower(): ", current_song['name'].lower())
                    if (current_search.lower() == current_song['name'].lower()):
                        last_song = current_song['id']
                        valid_songs.append(last_song)
                        word = i    # increment outer while loop to start at the first word not in the valid song
            
            if len(valid_songs) > 0:
                #print("valid_songs: ", valid_songs)
                #print("songs: ", songs)
                #print("adding song: ", valid_songs[-1])
                songs.append(valid_songs[-1])   # add the song to the song list to return
                valid_songs = []
            
        current_words = current_search.split()
        if current_words[-1] == search_list[-1]:
            break

    # create the playlist
    embed_link = create_playlist(songs, search_str, playlist_name)
    
    #return json.dumps(songs)
    return embed_link   # not sure if it needs the json.dumps() ?

## CREATE A PLAYLIST WHERE THE FIRST LETTER OF EACH SONG
## CORRELATES TO A USER INPUTTED STRING
@app.route('/getByLetter/<search_str>/<playlist_name>')
def search_letter(search_str : str, playlist_name="your playlist") -> list :
    # loop through words in search_str to find matching songs
    songs = []

    for i in range(len(search_str)):
        # current character
        current_char = search_str[i]
        #print("current_char:", current_char)

        # as long as the character is not a space, results = character
        #if current_char != ' ':
        if current_char.isalpha():
            results = sp.search(q=current_char, type='track')
            random_num = random.randrange(10)
            next_song = results['tracks']['items'][random_num]['id']

            songs.append(next_song)

    # create the playlist
    embed_link = create_playlist(songs, search_str, playlist_name)
    
    #return songs
    return embed_link

def create_playlist(songs : list, description: str, playlist_name: str) -> str:
    #songs = json.loads(songs)
    playlist = sp.user_playlist_create(username, playlist_name, public=True, description=description)
    #print(playlist)

    sp.user_playlist_add_tracks(username, playlist['id'], songs)

    embed_link = 'https://open.spotify.com/embed/playlist/' + playlist['id']
    return embed_link

#search_description = "PLEASE WORK"
#search2_description = "HELLO"
#results = search_title(search_description, "test playlist") 
#results2 = search_letter(search2_description)

#for song in results2:
#    print(song)  # song['album']['name'], song['album']['artists'][0]['name']

#create_playlist(results, search_description, "testing testing")
#create_playlist(results2, search2_description, "testing testing")
