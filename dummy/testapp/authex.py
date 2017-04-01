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
	results = sp.current_user_saved_tracks()
	for item in results['items']:
		track = item['track']
		print track['name'] + ' - ' + track['artists'][0]['name']
else:
	print "Can't get token for", username