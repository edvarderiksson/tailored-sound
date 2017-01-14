# app.py class deals with user input and Flask output
# @Author Andrea Simes @Author Edvard Eriksson


from flask import Flask, request, render_template, redirect, g, redirect, Response, url_for, flash, make_response, session 

import os
import urllib
import ast
from unicodedata import normalize

import tailor as tlr
import tester as tester
import testauth as testauth
import base64 # temp
import json # temp
import requests # temp

'''
*****Encoding spaces*****
Encode spaces from input with the hex code %20 or +
'''

# Globals
current_songs = []
with open("key.json") as json_data_file:
        key = json.load(json_data_file)


# links to keys
CLIENT_ID = key['CLIENT_ID'] 
CLIENT_SECRET = key['CLIENT_SECRET']

# Create templates folder
tmpl_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_fldr, static_url_path="")
app.secret_key = os.urandom(24)
# Loads main page and accepts user input
@app.route("/", methods = ['GET','POST'])
def landing_page():
	if request.method == 'GET':
		return render_template('landing.html')
	elif request.method == 'POST':
		query = request.form['text']
		return redirect(url_for('playlist', query = query))
	
# Displays playlist on playlist page
@app.route('/playlist/<query>', methods = ['GET','POST'])
def playlist(query):
	if request.method == 'GET':
		current_songs = tester.auth_tester(query)
		session['songs'] = current_songs
		return render_template('playlist.html', songs=current_songs)

	elif request.method == 'POST':
		#print('hi')
		playlist_name = request.form['text']
		session['playlist_name']=playlist_name
		return testauth.index()

#routing for "Add playlist to Spotify" button on playlist results template page
@app.route('/playlist', methods=['POST'])
def auth():
	return testauth.index()

# callback function that runs after Spotify redirects here after a successful user authentication
@app.route("/addplaylist/q") # make sure to add this url ("http://127.0.0.1:5000/addplaylist/q") to your Spotify Developers My Apps page
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



if __name__ == "__main__":
	app.run(debug=True)