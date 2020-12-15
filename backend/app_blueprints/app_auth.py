import logging
from models import app, User
from flask_security import Security
from flask import Blueprint, current_app, request
from flask_login import user_logged_in
from jose import jwt
import config
import requests

# define the blueprint variable
app_auth_blueprint = Blueprint("app_auth", __name__)
from bson.json_util import dumps


@app_auth_blueprint.route("/login", methods=["POST"])
def login(name=None):
    req = request.get_json()

    # Getting jwt key
    r = requests.get(url=config.COTTER_JWKS_URL)
    data = r.json()
    current_app.logger.info(data)
    public_key = data["keys"][0]
    # Getting access token and validate it
    token = req["oauth_token"]["access_token"]
    resp = jwt.decode(
        token, public_key, algorithms="ES256", audience=config.COTTER_API_KEY
    )
    current_app.logger.info(resp)
    user = User.create_find_user(resp["identifier"])
    # return details, then add token if needed
    if user:
        token = user.create_access_token()
        return (
            dumps(
                {
                    "ok": True,
                    "message": "Authenticated",
                    "userToken": token,
                    "userId": str(user.id),
                    "expiresIn": config.JWT_ACCESS_TOKEN_EXPIRES,
                    "userEmail": user.email,
                }
            ),
            200,
        )
    return (
        dumps({"ok": False, "message": "Invalid username or password"}),
        401,
    )
