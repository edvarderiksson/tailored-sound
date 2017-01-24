
import json
import requests
import sort as srt

def get_mood_songs(query, exclude):

	full_query = query #+ "%20"+"NOT"+"%20"+"blues"
	inp = {'q':full_query,'type':'track','limit':'20'}
	r = requests.get('https://api.spotify.com/v1/search', params=inp)
	data = json.loads(r.text)

	print(data)

get_mood_songs("roadhouse NOT Blues", "metal")