@app.errorhandler(Exception)
def handle_exception(e):
    be_logger.exception("An error occurred: %s", e)
    return str(e), 500
