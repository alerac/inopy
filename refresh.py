"""
	Copyright © 2023 Alexandre Racine <https://alex-racine.ch>

	This file is part of Inopy.

	Inopy is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

	Inopy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License along with Inopy. If not, see <https://www.gnu.org/licenses/>.

	-------------------------------------------------------------------------------------

	DISCLAIMER: parts of this code and comments blocks were created
	with the help of ChatGPT developped by OpenAI <https://openai.com/>
	Followed by human reviewing, refactoring and fine-tuning.

	-------------------------------------------------------------------------------------

	This code uses the values from the configuration file to construct a request payload. 

	The refresh function sends a POST request to the Inoreader OAuth endpoint <https://www.inoreader.com/developers/oauth> using the payload and headers to handle the refresh token process.

	Then it extracts the refreshed bearer token and the new refresh token in order to use it in the replace() function of the main ino.py module.
"""

import requests
import json
import configparser

# Initialize a ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file 'config.ini'
config.read('config.ini')

# Get the 'endpoint' value from the 'Oauth' section in the configuration file
url = config.get('Oauth', 'endpoint')

# Prepare the payload for the request
payload = {
	"client_id": config.get('Oauth', 'client_id'),
	"client_secret": config.get('Oauth', 'client_secret'),
	"grant_type": "refresh_token",
	"refresh_token": config.get('Oauth', 'refresh_token')
}

# Set the headers for the request
headers = {"Content-type": "application/x-www-form-urlencoded"}

# Define a function named 'refresh' that handles the token refresh logic
def refresh():
	
	# Send a POST request to the specified URL with the payload and headers
	response = requests.post(url, data=payload, headers=headers)

	# Check the response status code
	if response.status_code == 200:
		print("Request was successful.")
	else:
		print("Request failed with status code:", response.status_code)

	# Parse the response data as JSON
	data = json.loads(response.text)

	# Extract the refreshed bearer token and new refresh token from the response data
	refreshed_bearer = data['access_token']
	new_refresh_token = data['refresh_token']

	'''
		Return the refreshed bearer token and the new refresh token 
		in order to use it in the replace() function of the main
		ino.py module.
	'''
	return (refreshed_bearer, new_refresh_token)