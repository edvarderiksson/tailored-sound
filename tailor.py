# Tailor deals with the low-level work and contains
# the algorithms that create the custom playlists
# based on input from the app.py class
# @Author Edvard Eriksson

import json
import requests
import setup as stp 


# returns parameters for search, defailt values, except for query
def get_params(query, tp='track', limit='50'):
	
	inp = {'q':query,'type':tp, 'limit': limit}

	return inp


# Method that finds (50) songs based on track input

def get_track_songs(query):
	r = requests.get('https://api.spotify.com/v1/search', params=get_params(query))
	data = json.loads(r.text)
	songs = []

	# Save all song uris to a list
	for i in range(0,len(data['tracks']['items'])):
		songs.insert(i, data['tracks']['items'][i]['uri'])
	# return list of uris
	return songs


# Method that finds (50) songs based on mood input




# Method that finds (50) songs based on year input




# Method that finds (50) songs based on lyrics input




# Method that finds (50) songs based on genre input




#**********************Hybrid Searches**************************





























