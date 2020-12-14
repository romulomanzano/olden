import logging
from models import app
from flask_security import Security, current_user, Blueprint, current_app, request
from flask_login import user_logged_in
import config
import workos

workos.api_key = config.WORK_OS_API_KEY
workos.project_id = config.WORK_OS_PROJECT_ID

# define the blueprint variable
app_auth_blueprint = Blueprint("app_auth", __name__)


@app_top_level_blueprint.route("/login", methods=["GET"])
def sso_login():
    if current_user.is_authenticated:
        return redirect("/dashboard")
    redirect_uri = config.API_ENDPOINT + "/auth/callback"
    redirect_url = workos.client.sso.get_authorization_url(
        redirect_uri=redirect_uri,
        state={},
        provider=workos.utils.connection_types.ConnectionType.GoogleOAuth,
    )
    return redirect(redirect_url)


@app_top_level_blueprint.route("/callback", methods=["GET"])
def sso_redirect():
    code = request.args.get("code")
    try:
        profile = client.sso.get_profile(code)
        user = User.objects.get(email=profile.email, active=True)
        if user:
            flask_security.utils.login_user(user)
            return redirect("/dashboard")
        return redirect("/login")
    except Exception as e:
        return redirect("/login")
