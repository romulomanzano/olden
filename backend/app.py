"""
Flask API exposing the core endpoints needed to interact with the external API calls (from the devices)
"""
from models import BlacklistedToken, jwt, app
from app_blueprints.app_auth import app_auth_blueprint


# register blueprints
app.register_blueprint(app_auth_blueprint, url_prefix="/auth")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
