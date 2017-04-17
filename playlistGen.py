import sys
import os
os.environ['SPOTIPY_CLIENT_ID']='a92054407df245de94c7a001e0bb6afc'
os.environ['SPOTIPY_CLIENT_SECRET']='01f002d3ef2e4501a5d09d4cabcbedcb'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'
import spotipy
import spotipy.util as util
sys.path.append('.')
from playlistFuncs import *

token = getAuth()
getTrackInfo(token)
