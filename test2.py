from flask import Flask, request, redirect, render_template
import requests
import os
import signal
import configparser
import webbrowser
import time

# Configuration parser for reading the config file
config = configparser.ConfigParser()
config.read('config.ini')

endpoint = config.get('Oauth', 'endpoint')
client_id = config.get('Oauth', 'client_id')
client_secret = config.get('Oauth', 'client_secret')
callback = config.get('Oauth', 'callback')
scope = config.get('Oauth', 'scope')
CSRF = config.get('Oauth', 'CSRF')

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

            config.set('Oauth', 'bearer', access_token)
            config.set('Oauth', 'refresh_token', refresh_token)
            with open('config.ini', 'w') as config_file:
                config.write(config_file)

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
    return ('proccess ended', time.sleep(5), os.kill(os.getpid(), signal.SIGINT))

def run_app():
    # Open the browser and start the Flask app
    webbrowser.open('http://localhost:5000')
    app.run()

if __name__ == '__main__':
    #app.run()
    run_app()