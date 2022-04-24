description = '''
Transfer Apple Music Library to Spotify Liked Songs.

Steps to do:
1. Go to https://soundiiz.com and sign up.
2. Connect Spotify and Apple Music to Soundiiz.
3. Press F12 and Navigate to tracks section.
4. Under network section in dev console, filter XHR requests and search for endpoint ending with /tracks. Click any one of it and check for "authorization" in Request Headers. Copy the part next to 'Bearer ' and keep it safe.
5. Now in Soundiiz, Filter Apple music songs and select any one of the songs and right click -> Add to library and select Spotify. In parallel, in network console, you'll be able to see a request ending with /add. Click on it and copy the request header value of 'x-csrf-token'.
6. Run the script with both the token as arguments for initiating the transfer process.
'''

import requests
import json
import os
import time
import argparse

dir_path = os.path.dirname(os.path.realpath(__file__))

def getTracksFromAppleMusic(token):
	headers = {
		'authorization': 'Bearer '+token,
		'content-type': 'application/json'
	}
	response = requests.get(url='https://soundiiz.com/v1/api/users/me/platforms/applemusicapp/tracks', headers = headers)
	if response.status_code == 200:
		return response.text
	return str(response.status_code) + "::" + response.text

def addTrackInSpotify(token, track):
	data = {
		'tracks': [track],
		'dest': 'spotify',
	}
	headers = {
		'Host' : 'soundiiz.com',
		'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0',
		'Accept' : '*/*',
		'Accept-Language' : 'en-US,en;q=0.5',
		'Accept-Encoding' : 'gzip, deflate, br',
		'Referer' : 'https://soundiiz.com/webapp/tracks',
		'content-type' : 'application/json',
		'mode' : 'cors',
		'x-csrf-token' : token,
		'x-requested-with' : 'XMLHttpRequest',
		'Origin' : 'https://soundiiz.com',
		'Content-Length' : '779',
		'Alt-Used' : 'soundiiz.com',
		'Connection' : 'keep-alive',
		'Cookie' : 'hl=en; _ga=GA1.2.622237265.1644552458; locale=en; __stripe_mid=1bd82303-8ed2-4b1b-87f3-68f9668f6d62a3a6cc; _gid=GA1.2.1983154852.1650774740; PHPSESSID=a2re5ovnmdhuu5u6b9e3pic7cu;uSIc=48f5a69c120d3f5e32a5f01c0fc6e64cf6c9638837a27ea9a316ebc8a281e26e; changelogdate=1647270532; socialDisplayed=true; _gat=1',
		'Sec-Fetch-Dest' : 'empty',
		'Sec-Fetch-Mode' : 'no-cors',
		'Sec-Fetch-Site' : 'same-origin',
		'Pragma' : 'no-cache',
		'Cache-Control' : 'no-cache'
	}
	response = requests.post(url='https://soundiiz.com/v1/webapi/track/add', headers=headers, data=json.dumps(data))
	if response.status_code >= 200 and response.status_code < 300:
		#print(str(response.status_code) + "::" + response.text)
		pass
	else:
		print('error: '+str(response.status_code) + "::" + response.text)

parser = argparse.ArgumentParser(description=description)
parser.add_argument('-b', '--BearerToken', help="Bearer token for authenticating listing track endpoint.", required=True)
parser.add_argument('-c', '--CSRFToken', help="CSRF Token for authenticating transfer endpoint.", required=True)

args = parser.parse_args()

response = getTracksFromAppleMusic(args.BearerToken)

data = json.loads(response)

tracks = data['data']
total = data['total']

count = 1

for track in tracks:
	print(str(count)+" out of "+str(total)+" - Title: "+str(track['title'])+" by "+str(track['artist']))
	addTrackInSpotify(args.CSRFToken, track)
	time.sleep(1)
	count+=1

