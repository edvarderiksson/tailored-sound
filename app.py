# app.py deals with user input and Flask output
# @Author Andrea Simes @Author Edvard Eriksson


from flask import Flask, request, render_template, redirect, g, redirect, Response, url_for, flash, make_response, session 

import os
import urllib
import ast
from unicodedata import normalize

import tailor as tlr
import setup as stp

# Create templates folder
tmpl_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
static_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app = Flask(__name__, template_folder=tmpl_fldr, static_folder=static_fldr)
app.secret_key = os.urandom(24)


# Loads main page and accepts user input
@app.route("/", methods=['GET','POST'])
def landing_page():
	if request.method == 'GET':
		return render_template('landing-options.html')
	elif request.method == 'POST':
		# dropdown will hold the value 'mood' or 'word'
		dropdown = request.form['dropdown']
		query = request.form['main-input']
		include = request.form['include']
		exclude = request.form['exclude']
		years = request.form['years']

		if (dropdown == 'word') and (years != ''):
			query = query + " year:" + years
		if (dropdown == 'word') and (include != ''):
			query = query + " genre:" + include
		if (dropdown == 'word') and (exclude != ''):
			query = query + " NOT " + exclude 
		return redirect(url_for('playlist', query=query, dropdown=dropdown))
	

# Displays playlist on playlist page
@app.route('/playlist/<query>+<dropdown>', methods=['GET','POST'])
def playlist(query, dropdown):
	try:
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
			playlist_name = request.form['text']
			session['playlist_name'] = playlist_name
			return stp.index()

	except IndexError:
		return render_template('error_page.html')


#routing for "Add playlist to Spotify" button on playlist results template page
@app.route('/playlist', methods=['POST'])
def auth():
	playlist_name = request.form['text']
	session['playlist_name'] = playlist_name
	return stp.index()


# callback function that runs after Spotify redirects here after a successful user authentication
@app.route("/addplaylist/q") # make sure to add this url ("http://127.0.0.1:5000/addplaylist/q") to your Spotify Developers My Apps page
def add_playlist():
	return stp.callback()

# Error handling for wrong url
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




if __name__ == "__main__":
       #app.run(debug=True)
       port = int(os.environ.get("PORT", 5000))
       app.run(host='0.0.0.0', port=port)
