#Authorization to read user's saved tracks
import sys
import spotipy
import spotipy.util as util #prompts user to login if necessary and returns the user token suitable for use with spotipy.Spotify constructor

scope = 'user-library-read'

if len(sys.argv) > 1:
	username = sys.argv[1]
else:
	print "Usage: %s username" % (sys.argv[0],) #similar to format
	sys.exit()

token = util.prompt_for_user_token(username, scope)

if token:
	sp = spotipy.Spotify(auth=token)
	offset = 0
	count = 50
	while(count==50):
		count = 0
		results = sp.current_user_saved_tracks(50,offset)
		for item in results['items']:
			count+=1
			track = item['track']
			print track['name'] + ' - ' + track['artists'][0]['name']
		offset+=50
else:
	print "Can't get token for", username
