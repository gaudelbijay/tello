import os
from flask import Flask

WEB_ADDRESS = '0.0.0.0'
WEB_PORT = 5000

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(PROJECT_ROOT, 'droneapp/templates')
STATIC_FOLDER = os.path.join(PROJECT_ROOT, 'droneapp/templates')

DEBUG = False

LOG_FILE = 'pytello.log'

app = Flask(__name__, template_folder=TEMPLATE, static_folder=STATIC_FOLDER)

if DEBUG:
    app.debug = DEBUG