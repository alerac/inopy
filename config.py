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

	This code consists of two main functions: get_config and create_file.

	The get_config function check if the config directory or the config file exist. If not it creates config directory and/or config file and then gets the configuration data.

	The create_file function is called if the configuration file should be created. It prompts the user to enter configuration details and save them in the config file.

	Finally the config function serves as a wrapper function that sets the paths and calls get_config to retrieve the configuration data.
	
=========================================================================================
"""

import json
import os
import logging
from logs import LogFile

# Set logs file
log_file = LogFile()

'''
================================================================
	Create a function to check if the config directory
	and the config file exist. 
	
	If the config file or the config directory don't exist
	create them.
	
	Read the config file and load its contents into a dictionary.

	Extract the necessary values from the config dictionary,
	create a dictionary of local variables and return it.
================================================================
'''

def get_config(config_path, config_file_path):
	
	if os.path.exists(config_path):
		logging.info(f'Found config directory at {config_path}')
		
		if os.path.exists(config_file_path):
			logging.info(f'Found config file at {config_file_path}!')
			pass
		
		else:

			# If the config file doesn't exist, create it.
			create_file(config_file_path)
	
	else:

		# If the config directory doesn't exist, create it
		os.mkdir(config_path)
		logging.info(f'{config_path} created!')

		create_file(config_file_path)
	
	# load config content
	with open(config_file_path) as config_file:
		config = json.load(config_file)
	
	# Extract the necessary values from the config dictionary
	bearer = config['oauth']['bearer']
	refresh_token = config['oauth']['refresh_token']
	endpoint = config['oauth']['endpoint']
	client_id = config['oauth']['client_id']
	client_secret = config['oauth']['client_secret']
	callback = config['oauth']['callback']
	scope = config['oauth']['scope']
	csrf = config['oauth']['csrf']
	home_url = config['oauth']['home_url']

	unread_counts_url = config['inoapi']['unread_counts_url']
	feeds_list_url = config['inoapi']['feeds_list_url']

	summary = config['notification']['summary']
	singular_article = config['notification']['singular_article']
	plural_articles = config['notification']['plural_articles']

	prod_status = config['prod']['status']
	browser_path = config['prod']['browser_path']
	host = config['prod']['host']
	port = config['prod']['port']
	
	variables = locals()
	return variables

'''
==========================================================
	Create a function to prompt the user to enter details
	for the configuration file.

	Create the configuration dictionary.
	
	Write the configuration dictionary to the config file.
==========================================================
'''

def create_file(config_file_path):
	
	config = {}

	# prompt user for configuration data
	print("\nEnter details about OAuth authentication: \n")

	endpoint = input("Enter OAuth endpoint: ")
	client_id = input("Enter your client id: ")
	client_secret = input("Enter your client secret: ")
	callback = input("Enter your callback URL: ")
	scope = input("Enter the API scope (e.g. read OR read write): ")

	print("\nEnter details about Inoreader API: \n")

	unread_counts_url = input("Enter URL for unread articles: ")
	feeds_list_url = input("Enter URL for feeds lists: ")

	print("\nEnter details about notification message: \n")

	summary = input("Enter summary (title) for notification: ")
	singular_article = input("Enter singular label if there is only one unread article (e.g. new article in feed): ")
	plural_articles = input("Enter plural label if there are many unread articles (e.g. new articles in feed): ")

	# Create the configuration dictionary
	config["oauth"] = {
		"bearer": "",
		"refresh_token": "",
		"endpoint": endpoint,
		"client_id": client_id,
		"client_secret": client_secret,
		"callback": callback,
		"scope": scope,
		"csrf": "4902358490258",
		"home_url": "http://localhost:5000"
	}

	config["inoapi"] = {
		"unread_counts_url": unread_counts_url,
		"feeds_list_url": feeds_list_url
	}

	config["notification"] = {
		"summary": summary,
		"singular_article": singular_article,
		"plural_articles": plural_articles
	}

	config["prod"] = {
		"status": "true",
		"browser_path": "/usr/bin/firefox",
		"host": "0.0.0.0",
		"port": "5000"
	}

	# Write the config data to the config file
	with open(config_file_path, "w") as file:
		json.dump(config, file, indent=4)

	#print(f"{config_file_path} created successfully!")
	logging.info(f'Created config file at {config_file_path}!')

'''
==============================================
	Create a function to set the paths for the
	config directory and file.
	
	Get the configuration data and return it.
==============================================
'''

def config():
	
	# Set the path of config file to
	# /HOME/USER/.config/inopy/config.json
	config_path = os.path.join(os.environ['HOME'], '.inopy/config')
	config_file = 'config.json'
	config_file_path = os.path.join(config_path, config_file)
	
	# Get and return the configuration data
	data = get_config(config_path, config_file_path)
	return data

if __name__ == '__main__':
	config = config()