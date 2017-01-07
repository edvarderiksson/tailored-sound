# tailor 
# @Author Edvard Eriksson @Author Andrea Simes


from flask import Flask, request, render_template 
import requests
import json
import base64
import os

# Create templates folder
tmpl_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_fldr)

@app.route("/", methods = ['GET','POST'])
def landing_page():
	if request.method == 'GET':
		return render_template('index.html')
	elif request.method == 'POST':
		query = request.form['text']
		# Change to another template later
		return redirect(url_for('.playlist', query = query))

# Specify path
@app.route("/playlist/<query>")
# Main method
def get_playlist(query):

	
	

















































