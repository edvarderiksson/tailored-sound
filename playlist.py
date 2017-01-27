from flask import Flask, request, redirect, g, render_template
import requests
import base64

# currently not used
# ideally where we would move the code from app.py to make more modular

def add_playlist(user_info):
	# https://developer.spotify.com/web-api/create-playlist/
	# url = POST https://api.spotify.com/v1/users/{user_id}/playlists
	# curl -X POST "https://api.spotify.com/v1/users/thelinmichael/playlists" -H
	# "Authorization: Bearer {your access token}" -H "Content-Type: application/json" --data "{\"name\":\"A New Playlist\", \"public\":false}"
	#gt = {'Content-Type':'application/json'}
	gt = "{\"name\":\"A New Playlist\",\"public\":false}"
	
	#encoded = base64.b64encode(CLIENT_ID+":"+CLIENT_SECRET) works in Python 2, but not Python 3
	headers = {'Authorization':'Bearer ' + user_info['access_token'], 'Content-Type':'application/json'}

	r = requests.post('https://api.spotify.com/v1/users/'+user_info['api']+'/playlists', data=gt, headers=headers)
	print("success" + r.text)

