"""
=========================================================================================
	
	Copyright © 2023 Alexandre Racine <https://alex-racine.ch>

	This file is part of Inopy.

	Inopy is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

	Inopy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License along with Inopy. If not, see <https://www.gnu.org/licenses/>.

=========================================================================================

	DISCLAIMER: parts of this code and comments blocks were created
	with the help of ChatGPT developped by OpenAI <https://openai.com/>
	Followed by human reviewing, refactoring and fine-tuning.

=========================================================================================

	The aim of this module is to refresh both OAuth 2.0 access and refresh tokens and update the configuration file with the refreshed tokens.

=========================================================================================
"""

'''
=====================================================
	Create a refresh function to refresh the bearer
	and refresh token in the config data

	*	Set the headers and prepare the payload
		data for the HTTP request

	*	Send a POST request to the specified
		endpoint with the payload and headers
	
	*	Check the response status code to determine
		if the request was successful
	
	*	Parse the response data as JSON and extract
		the refreshed bearer token and new refresh
		token from the response data
	
	*	Open the config file. Load the existing
		config data from the file and update the
		bearer token and refresh token in the config
		data
	
	*	Move the file pointer to the beginning of
		the file, write the updated config data back
		to the file, overwriting the existing content
	
	*	Truncate the file to remove any remaining
		content after the updated data
=====================================================
'''

import requests
import json
import logging
from logs import LogFile

# Set logs file
log_file = LogFile()

def refresh(config_path, endpoint, client_id, client_secret, refresh_token):
	headers = {"Content-type": "application/x-www-form-urlencoded"}
	
	payload = {
		"client_id": client_id,
		"client_secret": client_secret,
		"grant_type": "refresh_token",
		"refresh_token": refresh_token
	}
	
	response = requests.post(endpoint, data=payload, headers=headers)
	
	if response.status_code == 200:
		logging.info("Request was successful. Token was refreshed...")
	
	else:
		logging.debug(f'Request failed with status code: {response.status_code}')
	
	data = json.loads(response.text)

	refreshed_bearer = data['access_token']
	new_refresh_token = data['refresh_token']

	with open(config_path, 'r+') as config_file:
		config = json.load(config_file)

		config['oauth']['bearer'] = refreshed_bearer
		config['oauth']['refresh_token'] = new_refresh_token

		config_file.seek(0)
		json.dump(config, config_file, indent=4)
		config_file.truncate()