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

	Inopy retrieves unread articles from the Inoreader API <https://www.inoreader.com/developers> and sends a notification if there are any unread articles.

	It uses a config file to store OAuth authentication data, Inoreader API endpoints <https://www.inoreader.com/developers/api-endpoint> and notification data.

	It performs token refreshing process if the API request returns an unauthorized status code.

	Inopy is structured into functions and modules for making API requests, parsing response data, refreshing tokens, sending notifications and logging the processes.

	For more information about OAuth authentication, plase see <https://www.inoreader.com/developers/oauth>

=========================================================================================
"""

import requests
import json
import notif
import logging
from config import config
from oauth import run_app
from refresh import refresh
from logs import LogFile

# Set logs file
log_file = LogFile()

'''
===========================================
	Define functions to make an API request
	with bearer token and parse response
	data as JSON
===========================================
'''

def APIrequest(url, bearer):
	bearer_string = 'Bearer {}'.format(bearer)
	headers = {'Authorization': bearer_string}
	response = requests.get(url, headers=headers)
	return response

def getData(response):
	data = json.loads(response.text)
	return data

'''
===================================
	Initialize an empty message
	string for the notification
===================================
'''

message = ""

'''
===========================================
	Load configuration settings and
	retrieve necessary configuration values
===========================================
'''

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
singular_article = config['singular_article']
plural_articles = config['plural_articles']

'''
=========================================
	Create dictionaries and list to store
	unread counts, subscriptions and feed
	categories (folders)
=========================================
'''

unreadcounts = {}
subscriptions = {}
categories = []

# Make API request to get unread counts

try:
	unread_response = APIrequest(unread_counts_url, bearer)

except Exception as e:
	logging.debug(e)

'''
===================================================
	If the response status code is 403 (Forbidden):

	*	Run the Flask app to get a bearer token
	
	*	Load the updated configuration file
	
	*	Update the bearer token with the new value
		from the updated config and make a new API
		request with the updated bearer token
===================================================
'''

'''
======================================================
	If the response status code is 401 (Unauthorized):
	
	*	Refresh the bearer token
	
	*	Load the updated configuration file
	
	*	Update the bearer token with the new value
		from the updated config and make a new API
		request with the updated bearer token
======================================================
'''

'''
============================================
	If the response status code is 200 (OK):

	*	proceed with the code execution
============================================
'''

try:

	# Check for 403 error case
	if unread_response.status_code == 403:
		logging.info('Token not available: starting oauth process...')
		run_app()

		with open(config_path) as config_file:
			new_config = json.load(config_file)

		bearer = new_config['oauth']['bearer']

		unread_response = APIrequest(unread_counts_url, bearer)

	# Check for 401 error case
	elif unread_response.status_code == 401:
		logging.info('Token expired: starting refresh process...')
		refresh(config_path, endpoint, client_id, client_secret, refresh_token)

		with open(config_path) as config_file:
			new_config = json.load(config_file)

		bearer = new_config['oauth']['bearer']
		
		unread_response = APIrequest(unread_counts_url, bearer)

	# Proceed with the code execution
	elif unread_response.status_code == 200:
		logging.info('API request ok: retrieving data...')
		pass

except Exception as e:
	logging.debug(e)

# Make API request to get feeds list

try:
	feeds_list_response = APIrequest(feeds_list_url, bearer)

except Exception as e:
	logging.debug(e)

'''
=======================================
	Parse the responses data as JSON
	
	Iterate over the unread counts and
	subscriptions and store them in the
	respective dictionaries

	If the subscription has categories
	(is part of a folder) append the
	category in the categories list
=======================================
'''

feeds_list_data = getData(feeds_list_response)
unread_data = getData(unread_response)

for unread in unread_data['unreadcounts']:
	unread['count'] = int(unread['count'])
	if unread['count'] > 0:
		unreadcounts[unread['id']] = unread['count']

for subscribed in feeds_list_data['subscriptions']:
	if subscribed['categories']:
		if subscribed['categories'][0]['id'] not in categories:
			categories.append(subscribed['categories'][0]['id'])
	
	subscriptions[subscribed['id']] = subscribed['title']

'''
==================================================
	Iterate over the unreadcounts dictionary
	
	Determine the appropriate singular or
	plural notification label based on the
	count (e.g. new article or new articles)

	Include the unread feed in the notification
	only if it is not in the categories list.
	This is to avoid duplicates notifications
	for the unread feed and the folder in which
	the feed is.

	Do not include the reading-list in the
	notification
	
	If the unread_id exists in the subscriptions
	dictionary, get the title associated with it.
	Else extract the title from the unread_id.

	Finally append the count, new_articles label
	and title to the message string
==================================================
'''

for unread_id, count in unreadcounts.items():

	# Determine singular or plural notification label
	new_articles = singular_article if count == 1 else plural_articles
	count = str(count)

	# Do not include the categories and the reading-list in the notification
	if not unread_id in categories:
		if unread_id.split("/")[-1] == "reading-list":
			pass
		
		else:
		
			# Get the clean feed title
			if unread_id in (k for k,v in subscriptions.items()):
				title = next(v for k, v in subscriptions.items() if k == unread_id)
			
			else:
				title = unread_id.split("/")[-1]
		
			# Build the final notification message
			message = message + count + " " + new_articles + " " + title + "\n"
	else:
		pass

'''
====================================
	Send the notification for unread
	feeds only if the message string
	is set
====================================
'''

try:
	if message != "":
		notif.send_notification(summary, message)
		logging.info('Notification successfully sent!')

	else:
		logging.info('No unread articles. Notification not sent.')
		pass

except Exception as e:
	logging.debug(e)