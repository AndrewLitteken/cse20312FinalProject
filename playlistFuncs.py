import sys
import spotipy
import spotipy.util as util

class Song:
	def __init__(self, n, artist, aID,  genre):
		self.name = n
		self.art=artist
		self.artID = aID
		self.gen=genre
		self.acoust = ''
		self.dance = ''
		self.eng = ''
		self.loud = ''
		self.valence = ''

def getAuth(scope, username):
	token = util.prompt_for_user_token(username, scope)
	return token

def getTrackInfo(token):
	sp = spotipy.Spotify(auth=token)
	
	offset = 0
	count = 50
	print 'Collecting Tracks...'
	songInfo={}
	genreInfo={}
	genreArtist={}
	
	while (count==50):
		count=0;
		results = sp.current_user_saved_tracks(50,offset)
		tracks=[]
		
		for item in results['items']:
			track = item['track']
			artist = track['artists'][0]
		
			if artist['name'] not in genreInfo:
				info = sp.artist(artist['id'])
				genreInfo[artist['name']]=info['genres']
			genres =  genreInfo[artist['name']]
			count+=1
			song = Song(track['name'],artist['name'],artist['id'],genres)
			songInfo[track['id']]=song
			for genre in genres:
				if genre not in genreArtist:
					genreArtist[genre]=set()
				genreArtist[genre].add(song)
			tracks.append(track['id'])
		
		offset+=50
		features = sp.audio_features(tracks)
		
		if offset%100==0 and count==50:
			print str(offset)+' tracks collected...'
	
	print 'Collection of '+str(offset-50+count)+' tracks complete'
	return {'songData': songInfo, 'genreData': genreArtist}

#def createPlaylist():
	
