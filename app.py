# app.py deals with user input and Flask output
# @Author Andrea Simes @Author Edvard Eriksson


from flask import Flask, request, render_template, redirect, g, redirect, Response, url_for, flash, make_response, session 

import os
import urllib
import ast
from unicodedata import normalize

import tailor as tlr
import setup as stp
import base64 # temp
import json # temp
import requests # temp

# Create templates folder
tmpl_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_fldr, static_url_path="")
app.secret_key = os.urandom(24)


# Loads main page and accepts user input
@app.route("/", methods=['GET','POST'])
def landing_page():
	if request.method == 'GET':
		return render_template('landing-options.html')
	elif request.method == 'POST':
		dropdown = request.form['dropdown']
		print(dropdown)
		query = request.form['main-input']
		return redirect(url_for('playlist', query=query, dropdown=dropdown))
	

# Displays playlist on playlist page
@app.route('/playlist/<query>+<dropdown>', methods=['GET','POST'])
def playlist(query, dropdown):
	if request.method == 'GET':
		if dropdown == 'mood':
			current_songs = tlr.get_mood_songs(query)
			session['songs'] = current_songs
			return render_template('playlist.html', songs=current_songs)
		elif dropdown == 'word':
			current_songs = tlr.get_track_songs(query)
			session['songs'] = current_songs
			return render_template('playlist.html', songs=current_songs)
	elif request.method == 'POST':
		playlist_name = request.form['main-input']
		session['playlist_name'] = playlist_name
		return stp.index()


#routing for "Add playlist to Spotify" button on playlist results template page
@app.route('/playlist', methods=['POST'])
def auth():
	return stp.index()


# callback function that runs after Spotify redirects here after a successful user authentication
@app.route("/addplaylist/q") # make sure to add this url ("http://127.0.0.1:5000/addplaylist/q") to your Spotify Developers My Apps page
def add_playlist():
	return stp.callback()



if __name__ == "__main__":
	app.run(debug=True)
