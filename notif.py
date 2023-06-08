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

	This code uses the pydbus library to send notifications. It defines a function send_notification() that takes summary and body as parameters. 

	Then, it calls the Notify method to send a notification with the specified parameters.

	Note that this code assumes that the necessary dependencies are installed and that the D-Bus service for notifications is available on the system.
"""

from pydbus import SessionBus

'''
	Create a new session bus instance
	Get the .Notifications interface object from the bus
'''

def send_notification(summary, body):
	bus = SessionBus()
	notifications = bus.get('.Notifications')

	'''
		Call the Notify method on the notifications object to send a notification
		Parameters:
			- 'MyApp': The name of the application sending the notification
			- 0: The ID of the notification (0 means a new notification)
			- '': An optional icon name or path for the notification
			- summary: The summary text of the notification
			- body: The body text of the notification
			- []: A list of actions associated with the notification (empty in this case)
			- {}: A dictionary of hints for the notification (empty in this case)
			- 5000: The timeout duration in milliseconds for the notification (5000 ms = 5 seconds)
	'''
	notifications.Notify('Inopy', 0, '/opt/chrome-apps-icons/inoreader.png', summary, body, [], {}, 5000)