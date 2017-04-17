import sys
import spotipy
import spotipy.util as util

def getAuth():
	scope = 'user-library-read'
	username = raw_input('Enter your Spotify Username: ')
	token = util.prompt_for_user_token(username, scope)
	return token

def getTrackInfo(token):
	sp = spotipy.Spotify(auth=token)
	offset = 0
	count = 50
	print 'Collecting Tracks...'
	while (count==50):
		count=0;
		results = sp.current_user_saved_tracks(50,offset)
		tracks={}
		for item in results['items']:
			count+=1
			tracks[item['track']['id']]=item['track']['name']
		offset+=50
		features = sp.audio_features(tracks)
		if offset%100==0 and count==50:
			print str(offset)+' tracks collected...'
		elif count<50:
			print str(offset-50+count)+' tracks collected...'
	print 'Collection complete'
		#for item in features:
			#print tracks[item['id']]+'-'+str(item['valence'])
