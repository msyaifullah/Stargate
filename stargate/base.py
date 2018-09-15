import jwt
import string
import random
import logging
import datetime

from stargate.error import register_errors
from authentication import Authentication
from stargate.error.error_object_not_found import ObjectNotFoundError


class Startgate(object):
    """
        Collection of the Authentication action.
    """
    _authentication = None

    def __init__(self, app=None, authentication=None):
        """

        :param app:
        """
        # Register with application
        if app is not None:
            self.init_app(app, authentication)

    def init_app(self, app, authentication=None):
        """

        :param app:
        :param authentication:
        :return:
        """

        if authentication is None:
            raise Exception("Need authentication class")

        if app.config.get('SECRET_AUTH_KEY') is None:
            raise Exception("You need to set SECRET_AUTH_KEY")

        if app.config.get('SECRET_REFRESH_KEY') is None:
            raise Exception("You need to set SECRET_REFRESH_KEY")

        if app.config.get('SECRET_PASSWORD') is None:
            raise Exception("You need to set SECRET_PASSWORD")

        register_errors(app)
        self._authentication = authentication
        self._init_extension(app)

    def _init_extension(self, app):
        """

        :return:
        """
        if not hasattr(app, 'extensions'):
            app.extensions = dict()
        app.extensions['stargate'] = self

    def class_authentication(self):
        if self._authentication is None and not isinstance(self._authentication, Authentication):
            raise ObjectNotFoundError({
                "description": "Object authentication is missing"
            })

        return self._authentication


class StargateResponse(object):
    """
    Stargate response attribute
        :status_code:
        :body:
    """

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])


def encode_auth_token(secret, user_id, sender_id=None, recipients_id=None, algorithm='HS256', expiration=3600):
    """
    Generates the Auth Token
    :return: string
    """
    return _jwt_encode(secret, user_id, sender_id, recipients_id, algorithm=algorithm, expiration=expiration)


def encode_refresh_token(secret, user_id, sender_id=None, recipients_id=None, algorithm='HS256', expiration=30758400):
    """
    Generates the Refresh Token
    :return: string
    """

    return _jwt_encode(secret, user_id, sender_id, recipients_id, algorithm=algorithm, expiration=expiration)


def decode_auth_token(secret, auth_token, recipients_id=None):
    """
    Validates the auth token
    :param secret:
    :param auth_token:
    :param recipients_id:
    :return: integer|string
    """
    try:
        return _jwt_decode(auth_token=auth_token, secret=secret, recipients_id=recipients_id)
    except Exception, e:
        logging.error(e.message)
        raise


def decode_refresh_token(secret, auth_token, recipients_id=None):
    """
    Validates the auth token
    :param secret:
    :param auth_token:
    :param recipients_id:
    :return: integer|string
    """
    try:
        return _jwt_decode(auth_token=auth_token, secret=secret, recipients_id=recipients_id)
    except Exception, e:
        logging.error(e.message)
        raise


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generate random characters
    :param size:
    :param chars:
    :return:
    """
    verification_id = ''.join(random.choice(chars) for _ in range(size))

    return verification_id


def _jwt_decode(auth_token, secret, recipients_id=None):
    try:
        return jwt.decode(auth_token, secret, audience=recipients_id)
    except Exception as e:
        logging.error(e.message)
        raise


def _jwt_encode(secret, user_id, sender_id=None, recipients_id=None, algorithm='HS256', expiration=3600):
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration),  # (expiration time)
        'iat': datetime.datetime.utcnow(),  # (issued at)
        'sub': user_id,  # (subject)
    }

    if sender_id is not None:
        payload['iss'] = sender_id  # (issuer)

    if recipients_id is not None:
        payload['aud'] = recipients_id  # (audience)

    try:
        return payload, jwt.encode(
            payload,
            secret,
            algorithm=algorithm
        )
    except Exception as e:
        logging.error(e.message)
        raise
