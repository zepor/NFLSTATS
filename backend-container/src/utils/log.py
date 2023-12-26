import sys
import os
import logging
from logging.handlers import RotatingFileHandler

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, 'src')) 

be_logger = logging.getLogger('backend-logger')
be_logger.setLevel(logging.DEBUG)

log_dir = './logs/'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'app.log')
file_handler = RotatingFileHandler(log_file, maxBytes=10000000, backupCount=5)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)
be_logger.addHandler(file_handler)

# Set up logging to console
console_handler = logging.StreamHandler(sys.stdout)
console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_formatter)
be_logger.addHandler(console_handler)

# Example of logging environment variables or other info
be_logger.info('FLASK_APP: %s', os.getenv('FLASK_APP'))
be_logger.info('FLASK_DEBUG: %s', os.getenv('FLASK_DEBUG'))