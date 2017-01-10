# Sets up the keys and token for the api calls
# that require authentication
# @ Author Edvard Eriksson @ Author Andrea Simes

import json
import requests
import base64


with open("key.json") as json_data_file:
	key = json.load(json_data_file)


# links to keys
CLIENT_ID = key['CLIENT_ID'] 
CLIENT_SECRET = key['CLIENT_SECRET']
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