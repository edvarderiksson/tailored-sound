# Sets up the keys and token for the api calls
# that require authentication
# @ Author Edvard Eriksson @ Author Andrea Simes

from flask import Flask, request
import json
import requests
import base64
import ast

with open("key.json") as json_data_file:
	key = json.load(json_data_file)


	# links to keys
	CLIENT_ID = key['CLIENT_ID'] 
	CLIENT_SECRET = key['CLIENT_SECRET']

def basic_credentials():

	# Need to solve encoding error in order to make this work	
	# Get tokens
	gt = {'grant_type':'client_credentials'}
	
	#encoded = base64.b64encode(CLIENT_ID+":"+CLIENT_SECRET) works in Python 2, but not Python 3
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
	'''
	Think this is why the page reloads because the token expires?
	'''
	# eventually we will need handling for refreshing the token when it expires
	# read Spotify auth guide 

    # use the access token to access Spotify API
	authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
	user_profile_api_endpoint = "https://api.spotify.com/v1/me"
	profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
	profile_data = json.loads(profile_response.text)
	print(profile_data['href'])

	#***************IGNORE FOR NOW****************
	# This stuff might be helpful later to display user picture, other user info etc.
    # Get user playlist data
    #playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    #playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    #playlist_data = json.loads(playlists_response.text)
    #**********************************************
    
    # Dict of user info used to create playlist
	user_info = {}
	user_info['api']=profile_data['href']
	user_info['access_token']=access_token

    # Create empty playlist

	name = session.get('playlist_name', None)
	gt = json.dumps({"name":name,"public":False}) # this must be json as per Spotify's API
	headers = {'Authorization':'Bearer ' + user_info['access_token'], 'Content-Type':'application/json'}
	r = requests.post(user_info['api']+'/playlists', data=gt, headers=headers) # POST request to create playlist
	playlist_response = json.loads(r.text)
	playlist_id = playlist_response['id'] # find playlist id so we can later add songs

    # collect already found songs that were displayed before
	current_songs = session.get('songs', None)

    # add tracks to playlist
	url = user_info['api']+'/playlists/' + playlist_id + "/tracks" # as per Spotify api "https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks"
	data = json.dumps({"uris":current_songs}) # use current songs as the songs to add to playlist
	r = requests.post(url, data = data, headers = headers) # POST method to add songs to playlist we just created

	flash("Playlist added") # Flask flash message added so we can display feedback to user eventually 

	return render_template("playlist_loggedin.html",songs=current_songs) # render template again with songs we already found using tailor.py
	

	