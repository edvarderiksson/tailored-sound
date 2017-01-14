# app.py class deals with user input and Flask output
# @Author Andrea Simes @Author Edvard Eriksson


from flask import Flask, request, render_template, redirect, g, redirect, Response, url_for, flash, make_response, session 

import os
import urllib
import ast
from unicodedata import normalize

import tailor as tlr
import setup as stp
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
		playlist_name = request.form['text']
		session['playlist_name']=playlist_name
		return testauth.index()



#routing for "Add playlist to Spotify" button on playlist results template page
@app.route('/playlist', methods=['POST'])
def auth():
	return testauth.index()

# callback function that runs after Spotify redirects here after a successful user authentication
@app.route("/addplaylist/q") # make sure to add this url ("http://127.0.0.1:5000/addplaylist/q") to your Spotify Developers My Apps page
def add_playlist():
	return stp.callback()



if __name__ == "__main__":
	app.run(debug=True)