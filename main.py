"""`main` is the top level module for your Flask application."""

# Import the Flask Framework
from flask import Flask, request
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return "Message: [} - From: {}".format(request.args.get("Body", ""), request.args.get("From", ""))
    return "No POST"

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500
