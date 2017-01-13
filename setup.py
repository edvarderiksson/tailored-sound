# Sets up the keys and token for the api calls
# that require authentication
# @ Author Edvard Eriksson @ Author Andrea Simes

import json
import requests
import base64
import ast

def main():

	with open("key.json") as json_data_file:
		key = json.load(json_data_file)


	# links to keys
	CLIENT_ID = key['CLIENT_ID'] 
	CLIENT_SECRET = key['CLIENT_SECRET']


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


	