import sys
import os
os.environ['SPOTIPY_CLIENT_ID']='a92054407df245de94c7a001e0bb6afc'
os.environ['SPOTIPY_CLIENT_SECRET']='01f002d3ef2e4501a5d09d4cabcbedcb'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'
import spotipy
import spotipy.util as util
sys.path.append('.')
from playlistFuncs import *

username = raw_input('Enter your Spotify Username: ')
make=1
usertoken = getAuth('user-library-read', username)
playtoken = getAuth('playlist-modify-private', username) 
genreInfo = getTrackInfo(usertoken)
while make:
	songs = filterSongs(genreInfo)
	for index, song in enumerate(songs):
		print str(index+1)+'. '+song[1].name+" - "+song[1].album
	create_playlist=raw_input("\nWould you like to push this playlist to Spotify? Y/N: ")
	if create_playlist.lower()=='y':
		push_playlist(songs, playtoken)
	cont=raw_input("Would you like to make another playlist? Y/N: ")
	if cont.lower()=='y':
		make=1
	else:
		make=0
print("We hope you enjoy your playlists!")	

