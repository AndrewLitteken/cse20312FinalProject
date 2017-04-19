import sys
import spotipy
import spotipy.util as util

class Song:
	def __init__(self, n, artist, aID):
		self.name = n
		self.art=artist
		self.artID = aID
		self.acoust = ''
		self.dance = ''
		self.eng = ''
		self.speech= ''
		self.loud = ''
		self.valence = ''

def getAuth(scope, username):
	token = util.prompt_for_user_token(username, scope)
	return token

def getTrackInfo(token):
	sp = spotipy.Spotify(auth=token)
	
	offset = 0
	count = 50
	print '\nCollecting Tracks...'
	genreInfo={}
	genreArtist={}
	
	while (count==50):
		count=0;
		results = sp.current_user_saved_tracks(50,offset)
		tracks=[]
		songs=[]
		for item in results['items']:
			track = item['track']
			artist = track['artists'][0]
		
			if artist['name'] not in genreInfo:
				info = sp.artist(artist['id'])
				genreInfo[artist['name']]=info['genres']
			genres =  genreInfo[artist['name']]
			count+=1
			song = Song(track['name'],artist['name'],artist['id'])
			songs.append(song)
			tracks.append(track['id'])
		
		offset+=50
		features = sp.audio_features(tracks)
		for index, song in enumerate(songs):
			feature = features[index]
			for genre in genreInfo[song.art]:
                        	if genre not in genreArtist:
                                	genreArtist[genre]=set()
                        	genreArtist[genre].add(song)
			song.acoust = feature['acousticness']	
			song.dance = feature['danceability']
                	song.eng = feature['energy']
                	song.speech= feature['speechiness']
                	song.loud = feature['loudness']
                	song.valence = feature['valence']	
		if offset%100==0 and count==50:
			print str(offset)+' tracks collected...'
	
	print 'Collection of '+str(offset-50+count)+' tracks complete'
	return genreArtist

def filterSongs(genreInfo):
	genres=[]
	inex=raw_input('\nSelect genres to include or exclude? I or E: ')
	for item in genreInfo.keys():
                genres.append(item)
	if inex.lower()=='e':	
		genres=genreCutting(genres)
	else:
		genres=genreAdding(genres)
	tones=['study', 'dance', 'happy', 'sad', 'melancoly', 'fun', 'angry', 'calming',]	
	tone=toneSelect(tones)
	critera=loadCriteria(tone)
	songs = []
	for genre in genres:
		for song in genreInfo[genre]:
			if songSelect(song, criteria):
				songs.append(song)
	return songs

def genreCutting(genres):
	genre=raw_input('\nAre there genres you would like to exclude? (Enter "o" to see options, "l" to see what has been removed, "r" to start over, and "n" to end input): ') 
	removed_genres=[]
	genre=genre.lower()
	while genre!='n':
        	if genre=='o':
                	for item in genres:
                        	print item
                elif genre not in genres:
			print '\nGenre not in list\n'
		elif genre=='l':
			for item in removed_genre:
				print item
		elif genre=='r':
			for item in removed_genre:
				genres.append()
			removed_genre=[]
		else:
			genres.remove(genre)
			removed_genres.append(genre)
		genre=raw_input('Next genre: ')
                genre=genre.lower()
	return genres

def genreAdding(genres):
	genre=raw_input('\nAre there genres you would like to include? (Enter "o" to see options, "l" for current list, "c" to clear, and "n" to end input): ')
	genre=genre.lower()
	new_genres=[]
	while genre!='n':
                if genre=='o':
                        for item in genres:
                                print item
                elif genre=='l':
                        for item in new_genres:
                                print item
                elif genre=='c':
                        new_genres=[]  
                elif genre not in genres:
                        print '\nGenre not in list\n'
		else:
                        if genre not in new_genres:
				new_genres.append(genre)
        	genre=raw_input('Next genre: ')
                genre=genre.lower()
	return new_genres

def toneSelect(tones):
	print '\nThe available tones are: '
	for tone in tones:
		print tone
	tone = raw_input('\nEnter your desired tone: ').lower()
	while tone not in tones:
		tone=raw_input('Not valid tone, enter again: ').lower()
	return tone 

def loadCriteria(tone):
	criteria={}
	if tone=='study':
		criteria['acoust']=0
		criteria['dance']=0
		criteria['energy']=0
		criteria['loud']=0
		criteria['valence']=0
	elif tone=='dance':
		criteria['acoust']=0
                criteria['dance']=0
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='happy':
		criteria['acoust']=0
                criteria['dance']=0
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='sad':
		criteria['acoust']=0
                criteria['dance']=0
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='melancoly':
		criteria['acoust']=0
                criteria['dance']=0
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='fun':
		criteria['acoust']=0
                criteria['dance']=0
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='angry':
		criteria['acoust']=0
                criteria['dance']=0
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='calming':
		criteria['acoust']=0
                criteria['dance']=0
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	return criteria

def songSelect(song, criteria):
	return 1
