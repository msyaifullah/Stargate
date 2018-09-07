from functools import wraps
from flask import request
from flask import current_app as app

from stargate.error.error_auth import AuthError
from stargate.error.error_device import DeviceError

from stargate.authentication import BlacklistToken

import jwt


def check_auth(username, password):
    """
    This function is called to check if a username /
    password combination is valid.

    """
    return True


def check_auth_bearer(token):
    """

    :param token:
    :return:
    """
    try:
        if BlacklistToken.check_blacklist(token):
            raise AuthError({
                "code": "Unauthorized",
                "description": "Token blacklisted. Please log in again."
            })
        payload = jwt.decode(token, app.config.get('SECRET_KEY'))
        return True, payload
    except jwt.ExpiredSignatureError:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Signature expired. Please log in again."
        })
    except jwt.InvalidTokenError:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Invalid token. Please log in again."
        })


def check_auth_refresh(token):
    """

    :param token:
    :return:
    """
    try:
        if BlacklistToken.check_blacklist(token):
            raise AuthError({
                "code": "Unauthorized",
                "description": "Token blacklisted. Please log in again."
            })
        payload = jwt.decode(token, app.config.get('SECRET_REFRESH_KEY'))
        return True, payload
    except jwt.ExpiredSignatureError:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Signature expired. Please log in again."
        })
    except jwt.InvalidTokenError:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Invalid token. Please log in again."
        })


def authenticate():
    """
    Sends a 403 response that enables basic auth

    """
    raise AuthError({
        "code": "Unauthorized",
        "description": "You don't have access to this resource."
    })


def check_device(device):
    """
    This function is called to check if a device id is valid.

    """
    uuid = device.get('Device-Id')
    if not uuid:
        return False
    return True


def valid_device():
    """
    Sends a 400 response that required device id

    """

    raise DeviceError({
        "code": "Unauthorized Device",
        "description": "You don't have access to this resource."
    })


def requires_auth(f):
    """
    Decoration used in endpoints

    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        kwargs['payload'] = {'username': auth.username}
        return f(*args, **kwargs)

    return decorated


def requires_bearer_auth(f):
    """
    Decoration used in endpoints

    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        try:
            auth_type, auth_info = auth.split(None, 1)
            auth_type = auth_type.lower()
        except ValueError:
            return
        if auth_type == b'bearer':
            is_valid, payload = check_auth_bearer(auth_info)
            if not is_valid:
                return authenticate()
            kwargs['jwt_payload'] = payload
        else:
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def requires_refresh_auth(f):
    """
    Decoration used in endpoints

    """

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        try:
            auth_type, auth_info = auth.split(None, 1)
            auth_type = auth_type.lower()
        except ValueError:
            return
        if auth_type == b'refresh':
            is_valid, payload = check_auth_refresh(auth_info)
            if not is_valid:
                return authenticate()
            kwargs['jwt_payload'] = payload
        else:
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def requires_device(f):
    """
    Decoration used in endpoints

    """

    @wraps(f)
    def decorated(*args, **kwargs):
        device = request.headers
        if not device or not check_device(device):
            return valid_device()
        return f(*args, **kwargs)

    return decorated



