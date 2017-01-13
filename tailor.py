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

def get_mood_songs(query):
	inp = {'q':query,'type':'playlist', 'limit': '20'}
	r = requests.get('https://api.spotify.com/v1/search', params=inp)
	data = json.loads(r.text)

	all_songs = {}

	playlist_num = 0
	for playlist in range(0,len(data['playlists']['items'])):
		# *************************************
		# Code that deals with second request
		# Called from setup
		# *************************************
		url = data['playlists']['items'][playlist_num]['tracks']['href']
		track_response = requests.get(url, headers=stp.main())
		track_data = json.loads(track_response.text)
		playlist_num += 1
		song_num = 0

		for track in range(0,len(track_data['items'])):
			if track_data['items'][song_num]['track']['uri'] in all_songs:
				current_value = all_songs[track_data['items'][song_num]['track']['uri']]
				current_value += 1
				all_songs[track_data['items'][song_num]['track']['uri']] = current_value
			else:
				all_songs[track_data['items'][song_num]['track']['uri']] = 1
			#print(track_data['items'][z]['track']['uri'])
			#all_songs.append(track_data['items'][z]['track']['uri'])
			song_num += 1
			
	return srt.get_fifty(all_songs)
'''
	most_popular = []
	for key, value in all_songs.items():
		if value > 1:
			most_popular.append(key)

	return(most_popular)
'''








# Method that finds (50) songs based on year input




# Method that finds (50) songs based on lyrics input




# Method that finds (50) songs based on genre input




#**********************Hybrid Searches**************************





























