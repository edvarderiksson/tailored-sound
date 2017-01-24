# Tailor deals with the low-level work ad contains
# the algoithms tht create the custom playlists
# based on input from app.py class
# @Author Edvard Eriksson @Author Andrea Simes

import json 
import requests
import setup as stp 
import sort as srt 

# Method that finds 50 songs based on track input

def get_track_songs(query):
	parameters = {'q':query, 'type':'track','limit':'50'}
	r = requests.get('https://api.spotify.com/v1/search', params=parameters)
	data = json.loads(r.text)
	songs = []

	# Save all song uris to a list
	for i in range(0,len(data['tracks']['items'])):
		songs.insert(i, data['tracks']['items'][i]['uri'])

	return songs


