import json
from os import environ as env
from urllib.parse import quote_plus, urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import redirect, render_template, session, url_for, Blueprint
if ENV_FILE := find_dotenv():
    load_dotenv(ENV_FILE)
auth_blueprint = Blueprint('auth_blueprint', __name__)
auth_blueprint.secret_key = env.get("APP_SECRET_KEY")
def init_oauth(app):
    global oauth
    oauth = OAuth()
    oauth.init_app(app)
    oauth.register(
        "auth0",
        client_id=env.get("AUTH0_CLIENT_ID"),
        client_secret=env.get("AUTH0_CLIENT_SECRET"),
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
    )

@auth_blueprint.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth_blueprint.callback", _external=True)
    )

@auth_blueprint.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@auth_blueprint.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))