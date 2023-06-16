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

	The aim of this module is to send a notification using the Inopy application. It takes a summary and body as input and utilizes D-Bus (Desktop Bus) to establish a session bus connection.

=========================================================================================
"""

import os
from pydbus import SessionBus

'''
=========================================
	Define a function to send the
	notification when a new unread
	article is present in the feed

	*	Create a new session
		bus instance
	
	*	Get the .Notifications interface
		object from the bus
=========================================
'''

def send_notification(summary, body):
	bus = SessionBus()
	notifications = bus.get('.Notifications')

	'''
	==================================================================================
		Call the Notify method on the notifications object to send a notification with
		Parameters:

			* 'MyApp': The name of the application sending the notification
			* 0: The ID of the notification (0 means a new notification)
			* '': An optional icon name or path for the notification
			* summary: The summary text of the notification
			* body: The body text of the notification
			* []: A list of actions associated with the notification
			  (empty in this case)
			* {}: A dictionary of hints for the notification (empty in this case)
			* 5000: The timeout duration in milliseconds for the notification
			  (5000 ms = 5 seconds)
	==================================================================================
	'''
	icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icons/inoreader.png')
	notifications.Notify('Inopy', 0, icon, summary, body, [], {}, 5000)