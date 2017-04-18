import sys
import os
os.environ['SPOTIPY_CLIENT_ID']='a92054407df245de94c7a001e0bb6afc'
os.environ['SPOTIPY_CLIENT_SECRET']='01f002d3ef2e4501a5d09d4cabcbedcb'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'
import spotipy
import spotipy.util as util
sys.path.append('.')
from playlistFuncs import *

username = raw_input('Enter you Spotify Username: ')
token = getAuth('user-library-read', username)
trackInfo = getTrackInfo(token)
songInfo = trackInfo['songData']
genreInfo = trackInfo['genreData']
genre=raw_input('What genre would you like your playlist to be in? (Enter list to see options): ') 
if genre=='list':
	for item in genreInfo.keys():
		print item
#generatePlaylist
