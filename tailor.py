# Tailor deals with the low-level work and contains
# the algorithms that create the custom playlists
# based on input from the app.py class
# @Author Edvard Eriksson

import json
import requests
import setup as stp 
import sort as srt



# returns parameters for search, defailt values, except for query
#def get_params(query, tp='track', limit='50'):
	#if mood==True:
	#inp = {'q':query,'type':tp, 'limit': limit}
	#return inp


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

def get_mood_songs(query, token):
	authorization_header = {"Authorization":"Bearer {}".format(token)}
	inp = {'q':query,'type':'playlist', 'limit': '20'}
	r = requests.get('https://api.spotify.com/v1/search', params=inp)
	data = json.loads(r.text)
	#print(data['playlists']['items'][0]['tracks']['href'])
	#print(len(data['playlists']['items']))
	all_songs = []

	# add all songs from every playlist to the list
	
	#all_songs = []
	all_songs = {}

	i = 0
	# needs to be corrected
	for playlist in range(0,len(data['playlists']['items'])):
		# *************************************
		# Code that deals with second request
		# Called from setup
		# *************************************
		url = data['playlists']['items'][i]['tracks']['href']
		# url = "https://api.spotify.com/v1/users/holgar_the_red/playlists/5Lzif2bIMW8RiRLtbYJHU0/tracks"
		track_response = requests.get(url, headers=authorization_header)
		track_data = json.loads(track_response.text)
		#print(track_data['items'][0])
		i += 1
		z = 0
		for track in range(0,len(track_data['items'])):
			if track_data['items'][z]['track']['uri'] in all_songs:

				current_value = all_songs[track_data['items'][z]['track']['uri']]
				current_value += 1
				all_songs[track_data['items'][z]['track']['uri']] = current_value
			else:
				all_songs[track_data['items'][z]['track']['uri']]=1
			#print(track_data['items'][z]['track']['uri'])
			#all_songs.append(track_data['items'][z]['track']['uri'])
			z += 1

	most_popular = []
	for key, value in all_songs.items():
		if value > 1:
			most_popular.append(key)



	# replace array with dictionary and keep track of instances of track

	# save the first (50)

	# return the songs

	return(most_popular)







# Method that finds (50) songs based on year input




# Method that finds (50) songs based on lyrics input




# Method that finds (50) songs based on genre input




#**********************Hybrid Searches**************************





























