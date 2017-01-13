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
		#return render_template('playlist.html', songs=tlr.get_track_songs(query))

		current_songs = tester.auth_tester(query)
		session['songs'] = current_songs
		return render_template('playlist.html', songs=current_songs)
	elif request.method == 'POST':
		#print('hi')
		playlist_name = request.form['text']
		session['playlist_name']=playlist_name
		return testauth.index()

@app.route('/playlist', methods=['POST'])
def auth():
	print('hi')
	return testauth.index()

@app.route("/addplaylist/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
	auth_token = request.args['code']
	code_payload = {
		"grant_type": "authorization_code",
		"code": str(auth_token),
		"redirect_uri": "http://127.0.0.1:5000/addplaylist/q"
	}
	base64encoded = base64.b64encode((CLIENT_ID+":"+CLIENT_SECRET).encode())
	headers = {"Authorization": "Basic " + base64encoded.decode()}
	token_request = requests.post("https://accounts.spotify.com/api/token", data=code_payload, headers=headers)

    # Auth Step 5: Tokens are Returned to Application
	response_data = json.loads(token_request.text)
	access_token = response_data["access_token"]
	refresh_token = response_data["refresh_token"]
	token_type = response_data["token_type"]
	expires_in = response_data["expires_in"]
	print("expires in")
	print(expires_in)

    # Auth Step 6: Use the access token to access Spotify API
	authorization_header = {"Authorization":"Bearer {}".format(access_token)}

    # Get profile data
	user_profile_api_endpoint = "https://api.spotify.com/v1/me"
	profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
	profile_data = json.loads(profile_response.text)
	print(profile_data['href'])

    # Get user playlist data
    #playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    #playlists_response = requests.get(playlist_api_endpoint, headers=authorization_header)
    #playlist_data = json.loads(playlists_response.text)

    # Get random playlist tracks
    #url = "https://api.spotify.com/v1/users/holgar_the_red/playlists/5Lzif2bIMW8RiRLtbYJHU0/tracks"
    #random_response = requests.get(url, headers=authorization_header)
    #random_data = json.loads(random_response.text)
    
    # Combine profile and playlist data to display
    #display_arr = [profile_data] + playlist_data["items"]
    #display_arr = random_data
    
	user_info = {}
	user_info['api']=profile_data['href']
	user_info['access_token']=access_token

    # create empty playlist
	name = session.get('playlist_name', None)
	gt = json.dumps({"name":name,"public":False})
    #gt = {"name":"A New Playlist","public":False}
	print(gt)
	headers = {'Authorization':'Bearer ' + user_info['access_token'], 'Content-Type':'application/json'}

	r = requests.post(user_info['api']+'/playlists', data=gt, headers=headers)
	playlist_response = json.loads(r.text)
	playlist_id = playlist_response['id']

    # collect already found songs that were displayed before
	current_songs = session.get('songs', None)
    # add tracks to playlist
	url = user_info['api']+'/playlists/' + playlist_id + "/tracks"
	data = json.dumps({"uris":current_songs})
	r = requests.post(url, data = data, headers = headers)
    # "https://api.spotify.com/v1/users/{user_id}/playlists/{playlist_id}/tracks"

    #print(random_data)
    #return user_info
    
	flash("Playlist added")
    #print(get_flashed_messages())
	return render_template("playlist_loggedin.html",songs=current_songs)



if __name__ == "__main__":
	app.run(debug=True)