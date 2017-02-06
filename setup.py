# Sets up the keys and token for the api calls
# that require authentication
# @ Author Edvard Eriksson @ Author Andrea Simes

from flask import Flask, request, redirect, g, render_template, session, flash
import json
import requests
import base64
import ast
import os

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

# with open("key.json") as json_data_file:
       # key = json.load(json_data_file)



'''
Anything that deals with API calls goes in this file

'''

# links to keys
# CLIENT_ID = key['CLIENT_ID'] 
CLIENT_ID = 'CLIENT_ID' in os.environ
# CLIENT_SECRET = key['CLIENT_SECRET']
CLIENT_SECRET = 'CLIENT_SECRET' in os.environ

def basic_credentials():

	gt = {'grant_type':'client_credentials'}
	
	raw = CLIENT_ID+":"+CLIENT_SECRET
	pre_encoded = raw.encode('ascii')
	encoded = base64.b64encode(raw.encode())
	encoded = encoded.decode("utf-8") 
	headers = {'Authorization':'Basic '+encoded}
	r = requests.post('https://accounts.spotify.com/api/token', data=gt, headers=headers)
	result = r.text
	token = ast.literal_eval(result)['access_token']
	authorization_header = {"Authorization":"Bearer {}".format(token)}

	return authorization_header

def callback():

    # requests refresh and access tokens
	auth_token = request.args['code']
	code_payload = {
		"grant_type": "authorization_code",
		"code": str(auth_token),
		"redirect_uri": "http://127.0.0.1:5000/addplaylist/q"
	}
	base64encoded = base64.b64encode((CLIENT_ID+":"+CLIENT_SECRET).encode())
	headers = {"Authorization": "Basic " + base64encoded.decode()}
	token_request = requests.post("https://accounts.spotify.com/api/token", data=code_payload, headers=headers)

    # token information
	response_data = json.loads(token_request.text)
	access_token = response_data["access_token"]
	refresh_token = response_data["refresh_token"]
	token_type = response_data["token_type"]
	expires_in = response_data["expires_in"]

    # use the access token to access Spotify API
	authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
	user_profile_api_endpoint = "https://api.spotify.com/v1/me"
	profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
	profile_data = json.loads(profile_response.text)
	print(profile_data['href'])
    
    # Dict of user info used to create playlist
	user_info = {}
	user_info['api']=profile_data['href']
	user_info['access_token']=access_token

    # Create empty playlist
	name = session.get('playlist_name', None)
	# this must be json as per Spotify's API
	gt = json.dumps({"name":name,"public":False}) 
	headers = {'Authorization':'Bearer ' + user_info['access_token'], 'Content-Type':'application/json'}
	r = requests.post(user_info['api']+'/playlists', data=gt, headers=headers)
	playlist_response = json.loads(r.text)

	# find playlist id so we can later add songs
	playlist_id = playlist_response['id'] 

    # collect already found songs that were displayed before
	current_songs = session.get('songs', None)

    # add tracks to playlist
	url = user_info['api']+'/playlists/' + playlist_id + "/tracks"
	# use current songs as the songs to add to playlist
	data = json.dumps({"uris":current_songs}) 
	# POST method to add songs to playlist we just created
	r = requests.post(url, data = data, headers = headers) 

	# Flask flash message added so we can display feedback to user eventually 
	flash("Playlist added!") 

	# render template again with songs we already found using tailor.py
	return render_template("playlist_loggedin.html",songs=current_songs) 


# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)


# Server-side Parameters
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/addplaylist/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()


auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    "client_id": CLIENT_ID
}


def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key,val) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

if __name__ == "__main__":
    app.run(debug=True,port=PORT)
