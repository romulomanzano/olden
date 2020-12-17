"""Defining JWT Manager that can be used across blueprints"""
from flask_jwt_extended import JWTManager
from models import BlacklistedToken
from utils import get_generic_logger
import mongoengine

jwt = JWTManager()
logger = get_generic_logger(__name__)


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
