# Tailor deals with the low-level work and contains
# the algorithms that create the custom playlists
# based on input from the app.py class
# @Author Edvard Eriksson

import json
import requests
import setup as stp 
import sort as srt



# returns parameters for search, defailt values, except for query
def get_params(query, tp='track', limit='50'):

	if mood==True:

	
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

def get_mood_songs(query):
	inp = {'q':query,'type':'playlist', 'limit': '100'}
	r = requests.get('https://api.spotify.com/v1/search', params=inp)
	data = json.loads(r.text)

	all_songs = []

	# add all songs from every playlist to the list

	i = 0
	# needs to be corrected
	for playlist in range(0,len(data['playlists'])):
		# *************************************
		# Code that deals with second request
		# Called from setup
		# *************************************
		for track in range(0,len(data['playlists'])):
			all_songs.insert(i, data['tracks']['items'][i]['uri'])
			i+=1


	# replace array with dictionary and keep track of instances of track

	# save the first (50)

	# return the songs

	return all_songs







# Method that finds (50) songs based on year input




# Method that finds (50) songs based on lyrics input




# Method that finds (50) songs based on genre input




#**********************Hybrid Searches**************************





























