import sys
import spotipy
import spotipy.util as util
import heapq

class Song:
	def __init__(self, n, spotID, alb,  artist, aID):
		self.name = n
		self.spID = spotID
		self.art=artist
		self.album = alb
		self.artID = aID
		self.acoust =0 
		self.dance =0
		self.energy =0
		self.speech= 0
		self.loud = 0
		self.valence = 0
		self.score = 0

def getAuth(scope, username):
	token = util.prompt_for_user_token(username, scope)
	return token

def getTrackInfo(token):
	sp = spotipy.Spotify(auth=token)
	
	offset = 0
	count = 50
	print '\nCollecting Tracks...'
	genreSong={}
	genreArtist={}
	
	while (count==50):
		count=0;
		results = sp.current_user_saved_tracks(50,offset)
		tracks=[]
		songs=[]
		for item in results['items']:
			track = item['track']
			artist = track['artists'][0]
		
			if artist['name'] not in genreArtist:
				info = sp.artist(artist['id'])
				genreArtist[artist['name']]=info['genres']
			count+=1
			song = Song(track['name'],track['id'],track['album']['name'], artist['name'],artist['id'])
			songs.append(song)
			tracks.append(track['id'])
		
		offset+=50
		features = sp.audio_features(tracks)
		for index, song in enumerate(songs):
			feature = features[index]
			for genre in genreArtist[song.art]:
                        	if genre not in genreSong:
                                	genreSong[genre]=set()
                        	genreSong[genre].add(song)
			song.acoust = feature['acousticness']	
			song.dance = feature['danceability']
                	song.energy = feature['energy']
                	song.speech= feature['speechiness']
                	song.loud = feature['loudness']
                	song.valence = feature['valence']	
		if offset%100==0 and count==50:
			print str(offset)+' tracks collected...'
	
	print 'Collection of '+str(offset-50+count)+' tracks complete'
	return genreSong

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
	criteria=loadCriteria(tone)
	length=int(raw_input("Number of songs in playlist: "))
	songs = []
	song_min=0
	song_min_name=''
	for genre in genres:
		for song in genreInfo[genre]:
			score=songSelect(song, criteria)
			if score and len(songs)<=length and (score, song) not in songs:
				song.score = score
				heapq.heappush(songs, (score, song))
			elif score:
				del songs[-1]
				heapq.heapify(songs)
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
		criteria['acoust']=0.700
		criteria['dance']=0.100
		criteria['speech']=0.100
		criteria['energy']=0.200
		criteria['loud']=-30
		criteria['valence']=0.100
	elif tone=='dance':
		criteria['acoust']=0.05
                criteria['dance']=0.500
		criteria['speech']=0.100
                criteria['energy']=0.850
                criteria['loud']=-5
                criteria['valence']=0.500
	elif tone=='happy':
		criteria['acoust']=0.005
                criteria['dance']=0.400
		criteria['speech']=0.100
                criteria['energy']=0.500
                criteria['loud']=10
                criteria['valence']=0.2
	elif tone=='sad':
		criteria['acoust']=[1, 0.400]
                criteria['dance']=[1, 0.200]
		criteria['speech']=[1, 0.100]
                criteria['energy']=[2, 0.150]
                criteria['loud']=[0, -10]
                criteria['valence']=[5, 0.100]
	elif tone=='melancoly':
		criteria['acoust']=0
                criteria['dance']=0
		criteria['speech']=0.100
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='fun':
		criteria['acoust']=0
                criteria['dance']=0
		criteria['speech']=0.100
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	elif tone=='angry':
		criteria['acoust']=0.005
                criteria['dance']=0.400
		criteria['speech']=0.100
                criteria['energy']=0.900
                criteria['loud']=-5
                criteria['valence']=0.300
	elif tone=='calming':
		criteria['acoust']=0
                criteria['dance']=0
		criteria['speech']=0.100
                criteria['energy']=0
                criteria['loud']=0
                criteria['valence']=0
	total=0
	for key in criteria.keys():
		total+=criteria[key][0]*criteria[key][1]
	criteria['total']=total
	return criteria

def songSelect(song, criteria):
	total=0
	comp_total=0
	value=criteria['acoust'][0]*song.acoust
	#if value>0.1:
	#	return 0
	total+=value
	value=criteria['dance'][0]*song.dance
	#if value>0.1:
	#	return 0
	total+=value
	value=criteria['speech'][0]*song.speech
        #if value>0.1:
        #        return 0
        total+=value
	value=criteria['energy'][0]*song.energy
        #if value>0.1:
        #        return 0
        total+=value
	value=criteria['loud'][0]*song.loud
        if value>20:
                return 0
	value=criteria['valence'][0]*song.valence
        if value>0.5:
                return 0
        total+=value
	if abs(criteria['total']-total)<1:
		return total
	return 0

def push_playlist(songs, token):
	sp = spotipy.Spotify(auth=token)
	name = raw_input("Playlist name: ")
	user = sp.current_user()
	usid = user['id']
	playlist=sp.user_playlist_create(usid, name, False)
	plid = playlist['id']
	songids=[]
	for song in songs:
		songids.append(song[1].spID)
	sp.user_playlist_add_tracks(usid, plid, songids)
