import os
from app import app
FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'true')
if FLASK_DEBUG == 'true':
    # Use Flask's built-in development server with debugging enabled
    print("Running in development mode...")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
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
        "timeout": 120,
        "accesslog": "-",
        "errorlog": "-",
        "worker_class": "gthread"
    }
    # Validate that essential option is set, else exit or set defaults
    if options["workers"] is None:
        print("Error: Environment variable for workers not set.")
        exit(1)
    StandaloneApplication(app, options).run()
