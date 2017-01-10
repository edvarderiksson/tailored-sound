# app.py class deals with user input and Flask output
# @Author Andrea Simes @Author Edvard Eriksson


from flask import Flask, request, render_template, redirect, g, redirect, Response, url_for, flash, make_response 

import os
import urllib
import ast
from unicodedata import normalize

import tailor as tlr 

# Create templates folder
tmpl_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_fldr, static_url_path="")

# Loads main page and accepts user input
@app.route("/", methods = ['GET','POST'])
def landing_page():
	if request.method == 'GET':
		return render_template('landing.html')
	elif request.method == 'POST':
		query = request.form['text']
		# get_songs(query)
		# Change to another template later
		return redirect(url_for('playlist', query = query))
	
# Displays playlist on playlist page
@app.route('/playlist/<query>')
def playlist(query):
	return render_template('playlist.html', songs=tlr.get_track_songs(query))


if __name__ == "__main__":
	app.run()