# Inopy

Inopy is a Python application that retrieves unread articles from the [Inoreader](https://www.inoreader.com) API and sends a notification if there are any.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Overview

It uses OAuth authentication for accessing the [API](https://www.inoreader.com/developers) and stores the authentication data in a JSON configuration file located at `/HOME/USER/.config/inopy/config.json`. The program is divided into multiple modules and functions for making API requests, parsing response data, refreshing tokens, and sending notifications.

The code is organized into the following modules:

- `ino.py`: The main module that retrieves unread articles, handles token refreshing, and sends notifications.
- `config.py`: Contains configuration settings used by other modules.
- `oauth.py`: Implements the OAuth authentication flow using Flask.
- `refresh.py`: Contains a `refresh` function for refreshing OAuth access and refresh tokens and updating the configuration file.
- `notif.py`: Provides a function for sending notifications using D-Bus (only tested with Cinnamon desktop environment).

## Installation

To use Inopy, you need to follow these steps:

1. Install the required dependencies by running the following command:

```bash
pip install requests pydbus flask waitress
```

2. Clone or download this repository.

3. Run the `ino.py` module the first time and set up the configuration file by providing the necessary OAuth, API endpoint and notifications details.

4. Run the `ino.py` module to retrieve unread articles and receive notifications.

## Usage

The first time `ino.py` module is run, it will check if `config.json` exists in `/HOME/USER/.config/inopy/`. If not it will prompt user for configuration details and create the `config.json` file. The file should contain the OAuth endpoint, client ID, client secret, callback URL, scope, CSRF value and home URL.

It should also contain the Inoreader API endpoints, notification labels, production status, browser path, host and port.

Once the configuration is set up, you can adapt some of the default values. Typically, check and if necessary adapt the `prod` section of the file. It defines whether the program is run in production or development mode.

To set a cron in Linux triggering the program for a notification, create a bash script containing the following code

```bash
#!/bin/bash
export DISPLAY=:0.0
export XAUTHORITY=/home/user/.Xauthority # adapt with your username
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus

python path_to_your_ino.py # adapt with the path to your program directory
```
and define the cron job pointing to the bash script created.

## License

Inopy is released under the GNU General Public License version 3 or later. You can redistribute it and/or modify it under the terms of the license. For more details, please refer to the [GNU General Public License](https://www.gnu.org/licenses/).