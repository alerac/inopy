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

	This module aims to provide an OAuth authentication flow using Flask.

	It sets up a web server that handles the authentication process, retrieves the access token and refresh token, and stores them in the configuration file.

	The module can be run in either production or development mode, and it opens a web browser to complete the authentication process.

=========================================================================================
"""

import requests
import webbrowser
import time
import json
import subprocess
import threading
import logging
from flask import Flask, request, redirect, render_template
from config import config
from waitress import serve
from logs import LogFile

# Set logs file
log_file = LogFile()

def run_app():

	'''
	===================================
		Load configuration values
		
		Extract values from the config
		dictionary
		
		Build the URL for authorization
	===================================
	'''

	conf = config()

	endpoint = conf['endpoint']
	client_id = conf['client_id']
	client_secret = conf['client_secret']
	callback = conf['callback']
	scope = conf['scope']
	CSRF = conf['csrf']
	home_url = conf['home_url']
	prod_status = conf['prod_status']
	browser_path = conf['browser_path']
	host = conf['host']
	port = conf['port']
	config_file_path = conf['config_file_path']

	url = 'https://www.inoreader.com/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope={}&state={}'.format(client_id, callback, scope, CSRF)

	'''
	==========================
		Initiate the Flask app
	==========================
	'''

	app = Flask(__name__)

	'''
	==================================
		When the home url is accessed:
		
		*	Redirect the user to the
			authorization URL
	==================================
	'''

	try:
		@app.route('/')
		def index():
			return redirect(url)

		logging.info('Redirecting to authorization URL...')

	except Exception as e:
		logging.debug(e)

	'''
	=====================================================
		When the oauth-callback url is accessed:

		*	Get the authorization code and other
			parameters from the callback URL
		
		*	Check CSRF validation token and if there
			is an error parameter in the URL
		
		*	Request bearer token and refresh token

		*	Save the bearer token and refresh token
			to the config file
		
		*	If process is successfull:
			
			*	render the success template with the
				response
		
		*	If CSRF failed:
			
			*	render the CSRF failure template
		
		*	If an error parameter is present in the URL:

			*	Render the OAuth error template
	=====================================================
	'''

	try:
		@app.route('/oauth-callback')

		def oauth_callback():
			authorization_code = request.args.get('code')
			csrf_check = request.args.get('state')
			error_param = request.args.get('error')

			csrf = True if csrf_check == CSRF else False
			error = True if error_param is not None else False

			if csrf and not error:
				access_token_url = endpoint
				
				# Prepare data to request bearer token
				payload = {
					'grant_type': 'authorization_code',
					'code': authorization_code,
					'client_id': client_id,
					'client_secret': client_secret,
					'redirect_uri': callback
				}

				# Request bearer token and refresh token
				response = requests.post(access_token_url, data=payload)
				
				if response.status_code == 200:
			
					access_token = response.json()['access_token']
					refresh_token = response.json()['refresh_token']

					with open(config_file_path, 'r+') as config_file:
						config = json.load(config_file)
						
						# Save the bearer token and refresh token to the config file
						config['oauth']['bearer'] = access_token
						config['oauth']['refresh_token'] = refresh_token
						
						config_file.seek(0)
						
						json.dump(config, config_file, indent=4)
						config_file.truncate()

				logging.info('New token obtained successfully...')
				return render_template('success.html', response=(access_token, refresh_token))
			
			else:
				if not csrf:
					logging.warning('CRSF validation failed...')
					return render_template('csrf-failed.html', response=(CSRF, csrf_check))
				
				elif error:
					error_content = request.args.get('error_description')
					logging.debug(error_content)
					return render_template('oauth-error.html', response=(error_param, error_content))
				
				else:
					pass

	except Exception as e:
		logging.debug(e)

	'''
	======================================
		When the shutdown url is accessed:

		*	Shut down the Flask server
			gracefully
	======================================
	'''

	try:
		@app.route('/shutdown')
		def shutdown():
			request.environ.get('werkzeug.server.shutdown')
			logging.info('Shutting down Flask server...')
			return 'Close this browser to terminate the process!'

	except Exception as e:
		logging.debug(e)

	'''
	======================================
		Define a function to start the
		Flask server using Waitress in
		production mode
	======================================
	'''

	def start_server():
		serve(app, host=host, port=port)

	'''
	======================================
		Define a function to start the
		production server inside a new
		thread.

		This is to ensure the server is
		actually already running before
		opening the web browser
	======================================
	'''

	def run_prod():
		logging.info('Running program in production mode...')
		server_thread = threading.Thread(target=start_server)
		server_thread.start()
		time.sleep(2)

		# Launch a separate browser process with a new profile
		subprocess.run([browser_path, "-CreateProfile", "new_profile", "-no-remote"])
		subprocess.run([browser_path, "-P", "new_profile", "-no-remote", home_url])

	'''
	======================================
		Define a function to start the
		development server inside a new
		thread.

		This is to ensure the server is
		actually already running before
		opening the web browser
	======================================
	'''

	def run_dev():
		logging.info('Running program in development mode...')
		server_thread = threading.Thread(target=start_server)
		server_thread.start()
		time.sleep(2)

		# Open the home URL in the default web browser
		webbrowser.open(home_url)
		app.run()

	'''
	======================================
		Determine whether to run the
		production or development server
		based on the config
	======================================
	'''
		
	try:
		if prod_status == "true":
			run_prod()

		else:
			run_dev()

	except Exception as e:
		logging.debug(e)

'''
======================================
	Run the application standalone
	if the script is executed but not
	imported
======================================
'''

if __name__ == '__main__':
	run_app()