import os
from app import app
# Determine the environment from the FLASK_ENV variable
flask_env = os.environ.get('FLASK_ENV', 'development')
if flask_env == 'development':
    # Use Flask's built-in development server with debugging enabled
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context="adhoc")
else:
    from gunicorn.app.base import Application
    class StandaloneApplication(Application):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()
        def load_config(self):
            for key, value in self.options.items():
                if key in self.cfg.settings and value is not None:
                    self.cfg.set(key.lower(), value)
        def load(self):
            return self.application
    options = {
        "bind": "0.0.0.0:8000",
        "workers": os.environ.get('WORKERS'),
        "certfile": os.environ.get('CERTFILE_PATH'),
        "keyfile": os.environ.get('KEYFILE_PATH'),
        "timeout": 120,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "gevent"
    }
    # Validate that essential options are set, else exit or set defaults
    for opt in ["workers", "certfile", "keyfile"]:
        if options[opt] is None:
            print(f"Error: Environment variable for {opt} not set.")
            exit(1)
    StandaloneApplication(app, options).run()
