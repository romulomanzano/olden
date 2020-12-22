"""
Flask API exposing the core endpoints needed to interact with the external API calls (from the devices)
"""
from models import BlacklistedToken, jwt, app
from app_blueprints.app_auth import app_auth_blueprint
from app_blueprints.app_organization import app_organization_blueprint
from app_blueprints.app_utils import app_utils_blueprint
from app_blueprints.app_profile import app_profile_blueprint
from app_blueprints.app_meet import app_meet_blueprint
from utils import get_generic_logger
import mongoengine

# register blueprints
app.register_blueprint(app_auth_blueprint, url_prefix="/auth")
app.register_blueprint(app_organization_blueprint, url_prefix="/organization")
app.register_blueprint(app_utils_blueprint, url_prefix="/utils")
app.register_blueprint(app_profile_blueprint, url_prefix="/profile")
app.register_blueprint(app_meet_blueprint, url_prefix="/meet")


logger = get_generic_logger(__name__)


@app.route("/debug-sentry")
def trigger_error():
    return 1 / 0


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decoded_token):
    jti = decoded_token["jti"]
    try:
        token = BlacklistedToken.objects(jti=jti).first()
        if token:
            return token.revoked
        return False
    except mongoengine.DoesNotExist as e:
        logger.error("Error finding JWT token: {}".format(e))
        return True


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
