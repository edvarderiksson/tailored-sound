# app.py class deals with user input and Flask output
# @Author Andrea Simes @Author Edvard Eriksson


from flask import Flask, request, render_template, redirect, g, redirect, Response, url_for, flash, make_response 

import os
import urllib
import ast
from unicodedata import normalize

import tailor as tlr
import tester as tester

'''
*****Encoding spaces*****
Encode spaces from input with the hex code %20 or +
'''

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
		return redirect(url_for('playlist', query = query))
	
# Displays playlist on playlist page
@app.route('/playlist/<query>')
def playlist(query):
	#return render_template('playlist.html', songs=tlr.get_track_songs(query))
	return render_template('playlist.html', songs=tester.auth_tester(query))


if __name__ == "__main__":
	app.run()