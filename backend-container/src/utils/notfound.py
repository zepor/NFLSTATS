from flask import jsonify, current_app
from src.utils.logandcatchexceptions import log_and_catch_exceptions

@log_and_catch_exceptions
def not_found(e):
    return jsonify(error=str(e)), 404

def init_app(app):
    app.register_error_handler(404, not_found)

