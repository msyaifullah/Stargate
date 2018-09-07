import jwt
import string
import random
import logging
import datetime

from stargate.helper import http_code

from authentication import BlacklistToken


class Startgate(object):
    """
        Collection of the Authentication action.
    """

    def __init__(self, app=None, environment=None):
        """

        :param app:
        :param environment:
        """
        self.app = app
        self.http = None
        # Register with application
        if app is not None:
            self.init_app(app, environment)

    def init_app(self, app=None, environment=None):
        pass

    @staticmethod
    def encode_auth_token(secret, user_id, sender_id, recipients_id, algorithm='HS256', expiration=3600):
        """
        Generates the Auth Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration),
            'iat': datetime.datetime.utcnow(),  # (issued at)
            'sub': user_id,  # (subject)
            'iss': sender_id,  # (issuer)
            'aud': recipients_id  # (audience)
        }
        try:
            return payload, jwt.encode(
                payload,
                secret,
                algorithm=algorithm
            )
        except Exception as e:
            logging.error(e.message)
            return payload, None

    @staticmethod
    def encode_refresh_token(secret, user_id, sender_id, recipients_id, algorithm='HS256', expiration=30758400):
        """
        Generates the Refresh Token
        :return: string
        """
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration),  # (expiration time)
            'iat': datetime.datetime.utcnow(),  # (issued at)
            'sub': user_id,  # (subject)
            'iss': sender_id,  # (issuer)
            'aud': recipients_id  # (audience)
        }
        try:
            return payload, jwt.encode(
                payload,
                secret,
                algorithm=algorithm
            )
        except Exception as e:
            logging.error(e.message)
            return payload, None

    @staticmethod
    def decode_auth_token(secret, auth_token, recipients_id):
        """
        Validates the auth token
        :param secret:
        :param auth_token:
        :param recipients_id:
        :return: integer|string
        """
        try:
            return jwt.decode(auth_token, secret, audience=recipients_id), http_code.HTTP_201_CREATED
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.', http_code.HTTP_400_BAD_REQUEST
        except jwt.InvalidTokenError, e:
            print(e.message)
            return 'Invalid token. Please log in again.', http_code.HTTP_400_BAD_REQUEST

    @staticmethod
    def decode_refresh_token(secret, auth_token, recipients_id):
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
                return jwt.decode(auth_token, secret, audience=recipients_id), http_code.HTTP_201_CREATED
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.', http_code.HTTP_400_BAD_REQUEST
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.', http_code.HTTP_400_BAD_REQUEST

    @staticmethod
    def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
        """
        Generate random characters
        :param size:
        :param chars:
        :return:
        """
        verification_id = ''.join(random.choice(chars) for _ in range(size))

        return verification_id


class StargateResponse(object):
    """
    Stargate response attribute
        :status_code:
        :body:
    """

    def __init__(self, initial_data):
        for key in initial_data:
            setattr(self, key, initial_data[key])
