import json
import os

def get_config(config_path, config_file_path):

    if os.path.exists(config_path):

        if os.path.exists(config_file_path):
            pass
        
        else:
            create_file(config_file_path)
    else:
        os.mkdir(config_path)
        print(f'{config_path} created!')
        create_file(config_file_path)

    # Load the config file
    with open(config_file_path) as config_file:
        config = json.load(config_file)

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

def create_file(config_file_path):
    config = {}
            
    # Ask user for input
    
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


    # Create nested JSON structure
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

    # Save config to a file
    with open(config_file_path, "w") as file:
        json.dump(config, file, indent=4)

    print(f"{config_file_path} created successfully!")

def config():
    config_path = os.path.join(os.environ['HOME'], '.config/inopy')
    config_file = 'config.json'
    config_file_path = os.path.join(config_path, config_file)
    data = get_config(config_path, config_file_path)
    return data