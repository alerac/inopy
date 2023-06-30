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

    This module aims to log the program processes.

=========================================================================================
"""

import os
import logging

# Setting the logs file
def LogFile():
    
    # Determine the user's home directory
    logs_dir = os.path.join(os.environ['HOME'], '.inopy/logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Configure logging
    log_file = os.path.join(logs_dir, "inopy.log")

    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', 
datefmt='%m/%d/%Y %I:%M:%S %p', filename=log_file, level=logging.DEBUG)