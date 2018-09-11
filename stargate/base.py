import jwt
import string
import random
import logging
import datetime

from stargate.helper import http_code


class Startgate(object):
    """
        Collection of the Authentication action.
    """

    def __init__(self, app=None):
        pass


class StargateResponse(object):
    """
    Stargate response attribute
        :status_code:
        :body:
    """

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])


class BlacklistToken(object):

    def __init__(self):
        pass

    @staticmethod
    def check_blacklist(auth_token):
        return False


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
        return _jwt_decode(auth_token=auth_token, secret=secret, recipients_id=recipients_id), http_code.HTTP_201_CREATED
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
        is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
        if is_blacklisted_token:
            return 'Token blacklisted. Please log in again.', http_code.HTTP_403_FORBIDDEN
        else:
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
