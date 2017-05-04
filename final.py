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

# Defining the "Song" class
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

# Creating the functions for proper data-analysis
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
			song.acoust = feature['acousticness']	
			song.dance = feature['danceability']
			song.energy = feature['energy']
			song.speech = feature['speechiness']
			song.loud = feature['loudness']
			song.valence = feature['valence']
			
			for genre in genreArtist[song.art]:	
				if genre not in genreSong:
					genreSong[genre]=set()
			genreSong[genre].add(song)
	
	return genreSong

def filterSongs(genres, tone, number):
	criteria=loadCriteria(tone)
	songs=[]
	for genre in genres:
		for song in genres[genre]:
			score=songSelect(song, criteria)
			# Andrew, I edited it like this so that there can never be repeats
			# If the error is persistent, it means that for the same song, 
			# there are multiple scores possible
			if (score, song) not in songs:
				if score and len(songs)<number:
					song.score = score
					heapq.heappush(songs, (score, song))
				elif score and score<songs[-1][0]:
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

# Begin Program

# Enter Spotify username here
username = "andrewlitteken"

# Retrieve User Information

token = getAuth('user-library-read playlist-modify-private', username)

# Initialize pygame
pygame.init()

# Begin background formatting
screen = pygame.display.set_mode((1200, 800))
background = pygame.Surface(screen.get_size())
background = background.convert()
pygame.display.set_caption('Spotify Playlist')

# Create and assign useful variables
font = pygame.font.SysFont("times", 19)
checkbox_x = 100
checkbox_y = 100
tone_startx = 700
tone_starty = 200
checkbox_size = 15
checkbox_thickness = 1

# Create and assign default variables for the user
tone = 'study'
number = 15

# Create and assign useful data structures
songInfo = {}
genreInfo = {}

# Get ready to launch program
run_spotify = True
background = pygame.image.load("spotify.jpg")
names_text = font.render("DONE BY: MARU CHOI, JIN KIM, ANDREW LITTEKEN", 1, (255, 255, 0))
collection_text = font.render("Music collection complete, Click to begin", 1, (255, 255, 0))

# Blit main (opening) screen to display
screen.blit(background, (160, 150))
screen.blit(names_text, (240, 625))
screen.blit(collection_text, (160, 725))

# Display the main (opening) screen 
pygame.display.flip()

# Have display first before retrieving genreInfo to ensure the main page has been loaded
print "Begin sleep!"
time.sleep(5);
print "End sleep!"

# Retrieve genre information based on the token -- the key to the username's Spotify account!
genreInfo = getTrackInfo(token)

# Launch program!
while run_spotify:
	events = pygame.event.get()
	clicked_begin_screen = False
	
	# While screen has not been clicked
	while not clicked_begin_screen:
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONDOWN:
				# Screen has been clicked! Move on to next "Select screen" -- user chooses inputs
				clicked_begin_screen = True
	
	# Refresh background -- black_background will "refresh" screen by drawing over
	black_background = pygame.image.load("black_screen.jpg")
	logo = pygame.image.load("logo.jpg")
	instructions_text = font.render("Choose as many genres as you want, but just one tone, then press 'Done'", 1, (255, 255, 0))
	
	# Blit the black_background to actual PyGame area
	screen.blit(black_background, (0, 0))
	screen.blit(logo, (1150, 1150))
	screen.blit(instructions_text, (45, 45))
	
	# Display the screen
	pygame.display.flip();
	
	# Begin preparing to draw on "Select screen"
	selectionMade = False
	y_spacer = int(0)
	
	while not selectionMade:
		# Establish tones for user to select:
		tones = ['study', 'dance', 'happy', 'sad', 'melancholy', 'fun', 'angry', 'calming']
		
		# Draw checkbox for the tones/genres!
		y_spacer = int(0)
		for tone in tones:
			pygame.draw.rect(black_background, (255, 51, 51), (tone_startx, checkbox_y+y_spacer, checkbox_size, checkbox_size), checkbox_thickness*2)
			screen.blit(black_background, (0, 0))
			y_spacer += int(15)
		
		side_increment=0	
		for genre in genreInfo.keys():
			pygame.draw.rect(black_background, (255, 51, 51), (checkbox_x + side_increment, checkbox_y+y_spacer, checkbox_size, checkbox_size), 
			checkbox_thickness*2)
			screen.blit(black_background, (0, 0))
			y_spacer += int(15)
			if checkbox_y + y_spacer > 800:
				y_spacer = 0
				side_increment += 50
		
		# Draw text for the genres!		
		y_spacer = int(0)
		for tone in tones:
			tones_text = font.render(tone, 1, (255, 225, 0))
			screen.blit(tones_text, (tone_startx + 15, tone_starty + y_spacer))
			y_spacer += int(15)
		
		side_increment =  0
		for genre in genreInfo.keys():
			genres_text = font.render(genre, 1, (255, 255, 0))
			screen.blit(genres_text, (checkbox_x + 15 + side_increment, checkbox_y + y_spacer))
			y_spacer+=15
			if checkbox_y + y_spacer + 15 > 800:	
				y_spacer = 0
				side_increment += 50
							
	
		# Draw a "done" button so that user can progress to next "Analysis" page!
		done_button = font.render("Done", 1, (255, 255, 255))
		
		# Blit the "done" button to screen
		screen.blit(done_button, (700, 100))
			
		# Display all - checkboxes, texts (labels), and "done" button
		pygame.display.flip()
		
		# Begin process to determine the checks
		choices_completed = False;
		events = pygame.event.get()
		
		# Define means of understanding user input
		genres_dict = {}
	
		while not choices_completed:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					print "x: "+str(x)+" y: "+str(y)
					
					# User presses the "done button"
					if x > 600 and y > 90 and y < 120:
						choices_completed = True

					# User selects a tone
					space = 15
					if x > tone_startx and x < tone_startx + checkbox_size:
						if y > tone_starty and y < tone_starty + space*1:
							tone = 'study'
						elif y > tone_starty + space*2 and y < tone_starty + space*3:
							tone = 'dance'
						elif y > tone_starty + space*4 and y < tone_starty + space*5:
							tone = 'happy'
						elif y > tone_starty + space*6 and y < tone_starty + space*7:
							tone = 'sad'
						elif y > tone_starty + space*8 and y < tone_starty + space*9:
							tone = 'melancholy'
						elif y > tone_starty + space*10 and y < tone_starty + space*11:
							tone += 'fun'
						elif y > tone_starty + space*12 and y < tone_starty + space*13:
							tone += 'angry'
						elif y > tone_starty + space*14 and y < tone_starty + space*15:
							tone += 'calming'
							print(tone)
							
					# User selects a genre
					side_increment = 0
					for index, genre in enumerate(genreInfo.keys()):
						if checkbox_y + space*index > 800:
							side_increment += int(50)
						if x > checkbox_x + side_increment and x < checkbox_x + checkbox_size + side_increment:
							if y > checkbox_y + space*index and y < checkbox_y + space*(index+1):
								genres_dict[genre] = genreInfo[genre]
							
		# Get out of "Selection screen"
		selectionMade = True
		
	# Reset screen for new "results screen" page
	black_background = pygame.image.load("black_screen.jpg")
	logo = pygame.image.load("logo.jpg")

	# Blit the "refreshed" screen
	screen.blit(black_background, (0, 0))
	screen.blit(logo, (650, 65))
	
	# Prepare to show the "Analysis screen"
	done_looking = False
	
	# Display the refreshed "Analysis screen"	
	pygame.display.flip();
	
	# Run the function to get the recommended songs
	songs = filterSongs(genreInfo, tone, number)
	  
	while not done_looking:
		
		
		# Reconfigure checkbox_x and checkbox_y
		checkbox_x = 500
		checkbox_y = 500
		
		# Draw yes/no checkboxes
		pygame.draw.rect(black_background, (255, 51, 51), (checkbox_x, checkbox_y, checkbox_size, checkbox_size), checkbox_thickness*2)
		pygame.draw.rect(black_background, (255, 51, 51), (checkbox_x, checkbox_y + 15, checkbox_size, checkbox_size), checkbox_thickness*2)
		
		# Blit yes/no checkboxes to screen
		screen.blit(black_background, (0, 0))
		# Draw a "done" button so that user can progress to next "Analysis" page!
		done_button = font.render("Done", 1, (255, 255, 255))
		# Blit the "done" button to screen
		screen.blit(done_button, (350, 600))
		# Include text for yes/no checkboxes
		yes_checkbox_t = font.render("Yes", 1, (0, 0, 255))
		no_checkbox_t = font.render("No", 1, (255, 0, 0))

		#
		song_startx = 100
		song_starty = 100

		# Display recommended songs to user
		y_spacer = int(0)
		counter = int(0)
		for song in songs:
			songs_text = font.render(str(counter)+". "+song[1].name, 1, (128, 255, 0))
			screen.blit(songs_text, (song_startx + 30, song_starty + y_spacer))
			counter += int(1)
			y_spacer += int(15)
			
		# Blit yes/no text to screen
		screen.blit(yes_checkbox_t, (checkbox_x + 15, checkbox_y))
		screen.blit(no_checkbox_t, (checkbox_x + 15, checkbox_y + 15))
		
		# Include instructions
		instructions_text = font.render("Choose to either push or not push these songs into a playlist", 1, (255, 255, 0))
		instructions2_text=font.render("in your account then press 'Done'", 1, (255, 255, 0))
		
		# Blit instructions to screen
		screen.blit(instructions_text, (45, 45))
		screen.blit(instructions2_text, (45, 90)) 
		
		# Actually display everything -- "done" button, the yes/no texts, the yes/no checkboxes
		pygame.display.flip()
		
		# Prepare to understand user input
		push_decision_made = False
		
		while not push_decision_made:
			for event in pygame.event.get():
				if event == pygame.MOUSEBUTTONDOWN:
					x, y = pygame.mouse.get_pos()
					# If User clicks "Yes"
					if x > checkbox_x and x < checkbox_x + checkbox_size:
						if y > checkbox_y and y < checkbox_y + y_spacer:
							push_playlist(songs, token)
															
					# User presses the "done button"
					if x > 350 and x<400 and y > 590 and y < 620:
						push_decision_made = True
		
		# Get out of while loop if User is done looking at songs
		done_looking = True
	
	# Refresh the page
	black_background = pygame.image.load("black_screen.jpg")
	logo = pygame.image.load("logo.jpg")
	
	# Blit the black_background to actual PyGame area
	screen.blit(black_background, (0, 0))
	screen.blit(logo, (650, 650))
	
	# Display the refreshed final screen
	pygame.display.flip()
	
	# Include "Thank you" message and our pictures
	thankyou_text = font.render("Thank you for participating in our demonstration of our project!", 1, (255, 255, 0))
	maru_choi = pygame.image.load("maru_choi.jpg")
	jin_kim = pygame.image.load("jin_kim.jpg")
	andrew_litteken = pygame.image.load("andrew_litteken.jpg")
	
	# Screen blit all -- our images, and thank you text
	screen.blit(maru_choi, (150, 150))
	screen.blit(jin_kim, (300, 300))
	screen.blit(andrew_litteken, (450, 450))
	screen.blit(thankyou_text, (0, 0))
	
	# Display the final "Thank you" screen -- our images and thank you text
	pygame.display.flip()
	
