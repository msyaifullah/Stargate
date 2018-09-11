from flask import request
from functools import wraps
from flask import current_app as app

from stargate.error.error_auth import AuthError
from stargate.error.error_general import GeneralError
from stargate.error.error_device import DeviceError

from stargate.base import BlacklistToken
from stargate.base import decode_auth_token
from stargate.base import decode_refresh_token
from jwt import InvalidIssuer
from jwt import InvalidAudience
from jwt import ExpiredSignature


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
        payload, status = decode_auth_token(app.config.get('SECRET_KEY'), token)
        return True, payload
    except InvalidIssuer:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Invalid Issuer. Please contact admin for this issues."
        })
    except InvalidAudience:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Invalid Audience. Please contact admin for this issues."
        })
    except ExpiredSignature:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Signature expired. Please log in again."
        })
    except Exception, e:
        raise GeneralError({
            "code": "Unauthorized",
            "description": "You get this message : {message}".format(message=e.message)
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
        payload, status = decode_refresh_token(app.config.get('SECRET_REFRESH_KEY'), token)

        return True, payload
    except InvalidIssuer:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Invalid Issuer. Please contact admin for this issues."
        })
    except InvalidAudience:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Invalid Audience. Please contact admin for this issues."
        })
    except ExpiredSignature:
        raise AuthError({
            "code": "Unauthorized",
            "description": "Signature expired. Please log in again."
        })
    except Exception, e:
        raise GeneralError({
            "code": "Unauthorized",
            "description": "You get this message : {message}".format(message=e.message)
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
