import copy
import inspect
import json
import random
import requests

from os import path

from flask import Blueprint, Flask, abort, render_template
from flask_cors import CORS

from api.backend_services import *
from api.frontend_services import *

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'

app.register_blueprint(backend_blueprint, url_prefix="/api/v1")
app.register_blueprint(frontend_blueprint, url_prefix="/api/v1")

# =====|
# Home |
# =====|
@app.route("/")
def home():
    return render_template('index.html')

if __name__ == "__main__":
    if not path.exists("export.json"):
        refresh_cache()

    config.league = open_cache()

    app.run(debug=True)
