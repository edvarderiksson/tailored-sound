# Tailor deals with the low-level work ad contains
# the algoithms tht create the custom playlists
# based on input from app.py 
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

def get_mood_songs(query):

	parsed_query = query.split()
	year_code = '7351'

	if parsed_query[((len(parsed_query))-1)] == year_code:
		


	print(parsed_query)
	
	parameters = {'q':query,'type':'playlist', 'limit': '20'}
	r = requests.get('https://api.spotify.com/v1/search', params=parameters)

	data = json.loads(r.text)

	all_songs = {}

	playlist_num = 0
	for playlist in range(0,len(data['playlists']['items'])):
		url = data['playlists']['items'][playlist_num]['tracks']['href']
		track_response = requests.get(url, headers=stp.basic_credentials())
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
			song_num += 1
			
	return srt.get_fifty(all_songs)

# Method that finds (50) songs based on genre input

def get_genre_songs(query):
	inp = {'q':query,'type':'genre', 'limit': '50'}
	r = requests.get('https://api.spotify.com/v1/search', params=inp)
	data = json.loads(r.text)

	# Save all song uris to a list
	for i in range(0,len(data['tracks']['items'])):
		songs.insert(i, data['tracks']['items'][i]['uri'])
	# return list of uris
	return songs
