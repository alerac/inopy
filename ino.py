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

	Inopy retrieves unread articles from the Inoreader API <https://www.inoreader.com/developers> and sends a notification if there are any unread articles.

	It uses a config file to store OAuth authentication data, Inoreader API endpoints <https://www.inoreader.com/developers/api-endpoint> and notification data.

	It performs token refreshing process if the API request returns an unauthorized status code.

	Inopy is structured into functions and modules for making API requests, parsing response data, refreshing tokens and sending notifications.

	For more information about OAuth authentication, plase see <https://www.inoreader.com/developers/oauth>
"""

import requests
import json
import notif
import time
import sys
import os
from config import config
from test2 import app, run_app
from refresh import refresh

"""
	Read the configuration file.

	Get the bearer token from the config
	and set it accordingly to Inoreader API
	specifications.

	Get the API endpoint URL from the config
	and send a GET request to the API.
"""

def APIrequest(url, bearer):
	bearer_string = 'Bearer {}'.format(bearer)
	headers = {'Authorization': bearer_string}
	response = requests.get(url, headers=headers)
	print(response.status_code)
	return response

# Parse the response as JSON
def getData(response):
	data = json.loads(response.text)
	return data

"""
	Refresh the bearer token if it expired.
	Update the bearer and refresh token
	in the config
"""

message = ""
config = config()

bearer = config['bearer']
unread_counts_url = config['unread_counts_url']
feeds_list_url = config['feeds_list_url']
config_path = config['config_file_path']
endpoint = config['endpoint']
client_id = config['client_id']
client_secret = config['client_secret']
refresh_token = config['refresh_token']
summary = config['summary']


# Make a request to get unread counts
unread_response = APIrequest(unread_counts_url, bearer)

"""
	If unauthorized (401) status code
	is received, refresh the bearer token
	and make a new request with the updated token.
"""

if unread_response.status_code == 403:
	print(unread_response.status_code)
	run_app()
	#new_config = config()
	#bearer = new_config['bearer']
	with open(config_path) as config_file:
		new_config = json.load(config_file)
	bearer = new_config['oauth']['bearer']
	print(bearer)
	unread_response = APIrequest(unread_counts_url, bearer)
	print(unread_response.text)

elif unread_response.status_code == 401:
	refresh(config_path, endpoint, client_id, client_secret, refresh_token)
	#new_config = config()
	#bearer = new_config['bearer']
	with open(config_path) as config_file:
		new_config = json.load(config_file)
	bearer = new_config['oauth']['bearer']
	print(bearer)
	unread_response = APIrequest(unread_counts_url, bearer)

elif unread_response.status_code == 200:
	pass
	
"""
	Get the list of feeds
	Parse the response data
	Parse the unread counts data
"""

feeds_list_response = APIrequest(feeds_list_url, bearer)
print(feeds_list_response)
feeds_list_data = getData(feeds_list_response)
unread_data = getData(unread_response)
print(feeds_list_data)
print('\n\n')
print(unread_data)

for item in unread_data['unreadcounts']:
	
	# Get the count of unread items
	count = int(item['count'])

	# If there are unread items
	# get the ID of the items
	
	if count > 0:
		ID = item['id']
		
		"""
			Loop through the feeds subscriptions.
			If the ID of unread feed is found in
			subscriptions (feeds), update ID with
			the feed title. Otherwise, extract the
			last part of the ID.

			This is because Inoreader feeds IDs are not
			human friendly labels.
		"""

		for item in feeds_list_data['subscriptions']:
			if ID in item['id']:
				ID = item['title']
			else:
				ID = ID.split("/")[-1]

		"""
			Use singular or plural forms
			depending on number of unread
			articles.

			Convert count to string and
			format the message.
		"""

		if count == 1:
			new_articles = config['singular_article']
		else:
			new_articles = config['plural_articles']
		count = str(count)
		message = message + count + " " + new_articles + " " + ID + "\n"
	else:
		pass

# Send notification if message is not empty.
if message != "":
	notif.send_notification(summary, message)
else:
	pass