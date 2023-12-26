import json
from os import environ as env
from urllib.parse import urlencode
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from flask import redirect, render_template, session, url_for, Blueprint
load_dotenv()
oauth = OAuth()

def init_oauth(app):
    global oauth
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

auth_blueprint = Blueprint('auth_blueprint', __name__)

@auth_blueprint.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth_blueprint.callback", _external=True)
    )

@auth_blueprint.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/auth")

@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("auth_blueprint.home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

@auth_blueprint.route("/")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))