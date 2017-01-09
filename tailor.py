# tailor 
# @Author Edvard Eriksson @Author Andrea Simes


from flask import Flask, request, render_template, redirect, g, redirect, Response, url_for, flash, make_response 
import requests
import json
import base64
import os
import urllib
import ast
from unicodedata import normalize


# Create templates folder
tmpl_fldr = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_fldr)


with open("key.json") as json_data_file:
	key = json.load(json_data_file)


# links to keys
CLIENT_ID = key['CLIENT_ID'] 
CLIENT_SECRET = key['CLIENT_SECRET']


@app.route("/", methods = ['GET','POST'])
def landing_page():
	if request.method == 'GET':
		print("hello1")
		return render_template('landing.html')
	elif request.method == 'POST':
		print("hello2")
		query = request.form['text']
		print(query)
		get_songs(query)
		# Change to another template later
		return redirect(url_for('landing.html', query = query))


# Specify path
@app.route("/playlist/<query>", methods=['POST'])
# Main method
def get_playlist():
	
	# Get tokens
	gt = {'grant_type':'client_credentials'}
	encoded = base64.b64encode(CLIENT_ID+":"+CLIENT_SECRET)
	headers = {'Authorization':'Basic '+encoded}
	#auth = base64.b64encode(CLIENT_ID + ":" + CLIENT_SECRET)
	#headers = {'Authorization': 'Basic  ' + auth}
	r = requests.post('https://accounts.spotify.com/api/token', data=gt, headers=headers)
	result = r.text
	token = ast.literal_eval(result)['access_token']

	# Make request with input
	r = requests.get('https://api.spotify.com/v1/search', params=get_params())

	# Convert json file into dict
	data = json.loads(r.text)
	
# @app.route("/<query>", methods=['GET'])
def get_songs(query):
	r = requests.get('https://api.spotify.com/v1/search', params=get_params(query))
	data = json.loads(r.text)
	print(data)

def get_params(query):
	# Get input
	# inp = {'q':query,'type':'track', 'limit': '10'}
	inp = {'q':query,'type':'track', 'limit': '50'}

	return inp 

# get_playlist()
if __name__ == "__main__":
	app.run()












































