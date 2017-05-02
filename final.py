#!/usr/bin/env python2.7

import pygame
import datetime
import time
import requests
import sys
import os
import json
import random		
import spotipy
import spotipy.util as util
import heapq
import sys
import os
os.environ['SPOTIPY_CLIENT_ID']='a92054407df245de94c7a001e0bb6afc'
os.environ['SPOTIPY_CLIENT_SECRET']='01f002d3ef2e4501a5d09d4cabcbedcb'
os.environ['SPOTIPY_REDIRECT_URI']='http://localhost:8888/callback'
sys.path.append('.')

from pygame.locals import *

# Running the other python programs
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
	
	return genreSong

def filterSongs(genres, tone, number):
	criteria=loadCriteria(tone)
	songs=[]
	for genre in genres:
		for song in genreInfo[genre]:
			score=songSelect(song, criteria)
			if score and len(songs)<number and (score, song) not in songs:
				song.score = score
				heapq.heappush(songs, (score, song))
			elif score:
				del songs[-1]
				heapq.heappush(songs, (score, song))
				heapq.heapify(songs)
	return songs

def loadCriteria(tone):
	criteria={}
	if tone=='study':
		criteria['acoust']=[2, 0.700]
		criteria['dance']=[1, 0.100]
		criteria['speech']=[2, 0.100]
		criteria['energy']=[4, 0.200]
		criteria['loud']=[0,-30]
		criteria['valence']=[2, 0.100]
	elif tone=='dance':
		criteria['acoust']=[1, 0.05]
                criteria['dance']=[3,0.500]
		criteria['speech']=[1, 0.100]
                criteria['energy']=[4,0.850]
                criteria['loud']=[0, -5]
                criteria['valence']=[2, 0.500]
	elif tone=='happy':
		criteria['acoust']=[1, 0.005]
                criteria['dance']=[1, 0.400]
		criteria['speech']=[2, 0.100]
                criteria['energy']=[3, 0.500]
                criteria['loud']=[0, 10]
                criteria['valence']=[4,0.4]
	elif tone=='sad':
		criteria['acoust']=[1, 0.400]
                criteria['dance']=[1, 0.200]
		criteria['speech']=[1, 0.100]
                criteria['energy']=[2, 0.150]
                criteria['loud']=[0, -10]
                criteria['valence']=[5, 0.100]
	elif tone=='melancholy':
		criteria['acoust']=[1, 0.700]
                criteria['dance']=[1, 0.450]
		criteria['speech']=[1, 0.020]
                criteria['energy']=[1, 0.400]
                criteria['loud']=[0, -10]
                criteria['valence']=[4, 0.200]
	elif tone=='fun':
		criteria['acoust']=[0, 0.050]
                criteria['dance']=[2, 0.500]
		criteria['speech']=[1, 0.100]
                criteria['energy']=[3, 0.800]
                criteria['loud']=[0, -7]
                criteria['valence']=[4, 0.600]
	elif tone=='angry':
		criteria['acoust']=[1, 0.005]
                criteria['dance']=[2, 0.400]
		criteria['speech']=[2, 0.100]
                criteria['energy']=[4, 0.900]
                criteria['loud']=[0, -5]
                criteria['valence']=[2,0.300]
	elif tone=='calming':
		criteria['acoust']=[1, 0.600]
                criteria['dance']=[2, 0.100]
		criteria['speech']=[1, 0.100]
                criteria['energy']=[2, 0.200]
                criteria['loud']=[0, -15]
                criteria['valence']=[4, 0.100]
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
	return abs(criteria['total']-total)

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

#username = raw_input('Enter your Spotify Username: ')
#make=1
username = "andrewlitteken"
token = getAuth('user-library-read playlist-modify-private', username)
#playtoken = getAuth('playlist-modify-private', username) 

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 800))
background = pygame.Surface(screen.get_size())
background = background.convert()
pygame.display.set_caption('Spotify Playlist')
font = pygame.font.SysFont("times", 19)
checkbox_x = 100
checkbox_y = 100
checkbox_size = 10
checkbox_thickness = 10
# Get ready to launch program

run_spotify = True

genreInfo = {}
songInfo = {}
tone='study'
number=15
print "authorization passed"
# Begin program
while run_spotify:
	#Basic setup of background
	background = pygame.image.load("spotify.jpg")
	screen.blit(background, (160, 150))
	names_text = font.render("DONE BY: MARU CHOI, JIN KIM, ANDREW LITTEKEN", 1, (255, 255, 0))
	screen.blit(names_text, (240, 625))
	pygame.display.flip();
	print "Getting songs"
	genreInfo = getTrackInfo(token)
	print "Got songs"
	events = pygame.event.get()
	clicked_begin_screen = False
	# Click screen to get started!
	for event in events:
		if event.type == pygame.MOUSEBUTTONDOWN:
				clicked_begin_screen = True
				black_background = pygame.image.load("black_screen.jpg")
				screen.blit(black_background, (0, 0))
				pygame.display.flip();
	while clicked_begin_screen:
		event = pygame.event.poll()
		# Draw Checkbox Rectangles
		pygame.draw.rect(black_background, (255, 51, 51), (checkbox_x, checkbox_y, checkbox_size, checkbox_size), checkbox_thickness*2)
		pygame.draw.rect(black_background, (255, 51, 51), (checkbox_x, checkbox_y+20, checkbox_size, checkbox_size), checkbox_thickness*2)
		pygame.draw.rect(black_background, (255, 51, 51), (checkbox_x, checkbox_y+40, checkbox_size, checkbox_size), checkbox_thickness*2)
		screen.blit(black_background, (0, 0))
		logo = pygame.image.load("logo.jpg")
		screen.blit(logo, (650, 650))
		
		# Include text descriptions -- tones
		tones = ['study', 'dance', 'happy', 'sad', 'melancholy', 'fun', 'angry', 'calming']
		temp = int(0)
		for tone in tones:
			tones_text = font.render(tone, 1, (255, 255, 51))
			screen.blit(tones_text, (checkbox_x + 30, checkbox_y + temp))
			temp+= int(20)
		
		# Include text descriptions -- genres
		temp = int(120)
		for genre in genreInfo.keys():
			genres_text = font.render(genre, 1, (255, 255, 0))
			screen.blit(genres_text, (checkbox_x + 30, checkbox_y + temp))
			temp+=int(20)
				
		# Display all
		pygame.display.flip()
		events = pygame.event.get()
		
		for event in events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				if x > checkbox_x and x < checkbox_x + checkbox_size:
					if y > checkbox_y and y < checkbox_y + 30:
						# tone = 'study'
						print ""
					elif y > checkbox_y + 30 and y < checkbox_y + 60:
						# tone = 'dance'
						print ""
					elif y > checkbox_y + 60 and y < checkbox_y + 90:
						# tone = 'happy'
						print ""
					elif y > checkbox_y + 90 and y < checkbox_y + 120:
						# tone = 'sad'
						print ""
					elif y > checkbox_y + 120 and y < checkbox_y + 150:
						# tone = 'melancholy'
						print ""
					elif y > checkbox_y + 150 and y < checkbox_y + 180:
						# tone = 'fun'
						print ""
					elif y > checkbox_y + 180 and y < checkbox_y + 210:
						# tone = 'angry'
						print ""
					elif y > checkbox_y + 210 and y < checkbox_y + 240:
						# tone = 'game'
						print ""
					elif y > checkboy_y + 240:
						# genre stuff
						print ""
		
		
		clicked_begin_screen = False
	
	# Reset screen for new "results screen" page
	screen.blit(background, (0, 0))
	reset_background = pygame.image.load("black_screen.jpg")
	screen.blit(background, (0, 0))
	pygame.display.flip();
	results_screen = True
	checkbox_x = 150
	checkbox_y = 150
	
	# Run the function to get the recommended songs
	songs = filterSongs(genreInfo, tone, number)
	
	# "Results screen" pops out to display the results
	while results_screen:
		temp = int(0)
		num = int(1)
		
		# Display recommended songs to user
		for song in songInfo.keys():
			songs_text = font.render(genre, 1, (255, 255, 0))
			screen.blit(str(num) + songs_text, (checkbox_x + 30, checkbox_y + temp))
			temp+=int(20)
			num+=int(1)
		
		# Display checkbox -- decision to push playlist or not
		pygame.draw.rect(reset_background, (255, 51, 51), (checkbox_x, checkbox_y, checkbox_size, checkbox_size), checkbox_thickness*2)
		pygame.draw.rect(reset_background, (255, 51, 51), (checkbox_x, checkbox_y+20, checkbox_size, checkbox_size), checkbox_thickness*2)
		screen.blit(background, (0, 0))
		logo = pygame.image.load("logo.jpg")
		screen.blit(logo, (650, 650))
		
		decision_text_yes = font.render("Yes", 1, (255, 255, 0))
		decision_text_no = font.render("No", 1, (255, 255, 0))
		
		screen.blit(decision_text_yes, (checkbox_x + 15, checkbox_y))
		screen.blit(decision_text_no, (checkbox_x + 15, checkbox_y+20))
		
		# Actually display everything
		pygame.display.flip()
		
		# If click -- make a decision
		events = pygame.event.get()
		for event in events:
			if event == pygame.MOUSEBUTTONDOWN:
				x, y = pygame.mouse.get_pos()
				if x > checkbox_x and x < checkbox_x + checkbox_size:
					if y > checkbox_y and y < checkbox_y < checkbox_size:
						# Push the playlist
						print ""
					elif y > checkbox_y + checkbox_size and y < checkbox_y + checkbox_size*2:
						# Do not push the playlist
						print ""
		
		# Say goodbye to the user!
	
	# End while loop
