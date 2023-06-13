from flask import Flask, request, redirect, render_template
from config import config
from waitress import serve
import requests
import os
import signal
import webbrowser
import time
import json
import subprocess
import threading

config = config()

endpoint = config['endpoint']
client_id = config['client_id']
client_secret = config['client_secret']
callback = config['callback']
scope = config['scope']
CSRF = config['csrf']
home_url = config['home_url']

prod_status = config['prod_status']
browser_path = config['browser_path']
host = config['host']
port = config['port']

config_file_path = config['config_file_path']

url = 'https://www.inoreader.com/oauth2/auth?client_id={}&redirect_uri={}&response_type=code&scope={}&state={}'.format(client_id, callback, scope, CSRF)

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url)

@app.route('/oauth-callback')

def oauth_callback():
    
    # Get the authorization code from the request URL
    
    authorization_code = request.args.get('code')
    csrf_check = request.args.get('state')
    error_param = request.args.get('error')

    csrf = True if csrf_check == CSRF else False
    error = True if error_param != None else False

    if csrf == True and error != True:

        # Exchange the authorization code for an access token
        access_token_url = endpoint
        payload = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': callback
        }

        response = requests.post(access_token_url, data=payload)

        # Parse the response to get the access token
        if response.status_code == 200:

            access_token = response.json()['access_token']
            refresh_token = response.json()['refresh_token']

            with open(config_file_path, 'r+') as config_file:
                # Load the JSON data from the file
                config = json.load(config_file)

                # Update the token value in the config data
                config['oauth']['bearer'] = access_token
                config['oauth']['refresh_token'] = refresh_token

                # Move the file pointer back to the beginning of the file
                config_file.seek(0)

                # Write the updated config data to the file
                json.dump(config, config_file, indent=4)
                config_file.truncate()

        return render_template('success.html', response=(access_token, refresh_token))

    else:

        # Redirect the user to a desired URL

        if csrf != True:
            return render_template('csrf-failed.html', response=(CSRF, csrf_check))

        elif error == True:
            error_content = request.args.get('error_description')
            return render_template('oauth-error.html', response=(error_param, error_content))

        else:
            pass

@app.route('/shutdown')
def shutdown():
    # Shutting down the Flask app gracefully
    #return ('proccess ended', time.sleep(5), os.kill(os.getpid(), signal.SIGINT))
    
    request.environ.get('werkzeug.server.shutdown')
    return 'Close this browser to terminate the process!'


'''def run_prod():

    # Create a new Firefox profile
    subprocess.run([browser_path, "-CreateProfile", "new_profile", "-no-remote"])

    # Launch Firefox with the new profile and open the URL
    subprocess.run([browser_path, "-P", "new_profile", "-no-remote", home_url])
    
    serve(app, host=host, port=port)'''

# Function to start the Flask server
def start_server():
    serve(app, host=host, port=port)

def run_prod():

    # Create a new thread for the Flask server
    server_thread = threading.Thread(target=start_server)

    # Start the Flask server thread
    server_thread.start()

    # Wait for the Flask server to start (adjust the delay as needed)
    time.sleep(2)

    # Create a new Firefox profile
    subprocess.run([browser_path, "-CreateProfile", "new_profile", "-no-remote"])

    # Launch Firefox with the new profile and open the URL
    subprocess.run([browser_path, "-P", "new_profile", "-no-remote", home_url])

def run_dev():

    # Create a new thread for the Flask server
    server_thread = threading.Thread(target=start_server)

    # Start the Flask server thread
    server_thread.start()

    # Wait for the Flask server to start (adjust the delay as needed)
    time.sleep(2)

    webbrowser.open(home_url)
    app.run()

def run_app():

    if prod_status == "true":
        print(prod_status)
        run_prod()
    else:
        print(prod_status)
        run_dev()

if __name__ == '__main__':
    #app.run()
    run_app()