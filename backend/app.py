"""
Flask API exposing the core endpoints needed to interact with the external API calls (from the devices)
"""
from models import BlacklistedToken, jwt, app
from app_blueprints.app_auth import app_auth_blueprint
from app_blueprints.app_virtual_events import app_events_blueprint

# register blueprints
app.register_blueprint(app_auth_blueprint, url_prefix="/auth")
app.register_blueprint(app_events_blueprint, url_prefix="/virtual_events")


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
