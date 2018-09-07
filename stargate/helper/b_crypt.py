from __future__ import absolute_import
from __future__ import print_function

from werkzeug.security import safe_str_cmp

try:
    import bcrypt
except ImportError as e:
    print('bcrypt is required to use Flask-Bcrypt')
    raise e

import hashlib

from sys import version_info

PY3 = version_info[0] >= 3


def generate_password_hash(password, rounds=None):
    """
        pw_hash = generate_password_hash('hunter2', 10)

    :param password: The password to be hashed.
    :param rounds: The optional number of rounds.

    :return:
    """
    return BCrypt().generate_password_hash(password, rounds)


def check_password_hash(pw_hash, password):
    """
        check_password_hash(pw_hash, 'hunter2') # returns True

    :param pw_hash: The hash to be compared against.
    :param password: The password to compare.
    :return:
    """
    return BCrypt().check_password_hash(pw_hash, password)


class BCrypt(object):
    _log_rounds = 12
    _prefix = '2b'
    _handle_long_passwords = False

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        '''Initalizes the application with the extension.

        :param app: The Flask application object.
        '''
        self._log_rounds = app.config.get('BCRYPT_LOG_ROUNDS', 12)
        self._prefix = app.config.get('BCRYPT_HASH_PREFIX', '2b')
        self._handle_long_passwords = app.config.get('BCRYPT_HANDLE_LONG_PASSWORDS', False)

    def _unicode_to_bytes(self, unicode_string):
        '''Converts a unicode string to a bytes object.

        :param unicode_string: The unicode string to convert.'''
        if PY3:
            if isinstance(unicode_string, str):
                bytes_object = bytes(unicode_string, 'utf-8')
            else:
                bytes_object = unicode_string
        else:
            if isinstance(unicode_string, unicode):
                bytes_object = unicode_string.encode('utf-8')
            else:
                bytes_object = unicode_string
        return bytes_object

    def generate_password_hash(self, password, rounds=None, prefix=None):
        """
        pw_hash = bcrypt.generate_password_hash('secret', 10)

        :param password: The password to be hashed.
        :param rounds: The optional number of rounds.
        :param prefix: The algorithm version to use.
        :return:
        """

        if not password:
            raise ValueError('Password must be non-empty.')

        if rounds is None:
            rounds = self._log_rounds
        if prefix is None:
            prefix = self._prefix

        # Python 3 unicode strings must be encoded as bytes before hashing.
        password = self._unicode_to_bytes(password)
        prefix = self._unicode_to_bytes(prefix)

        if self._handle_long_passwords:
            password = hashlib.sha256(password).hexdigest()
            password = self._unicode_to_bytes(password)

        salt = bcrypt.gensalt(rounds=rounds, prefix=prefix)
        return bcrypt.hashpw(password, salt)

    def check_password_hash(self, pw_hash, password):
        """
            pw_hash = bcrypt.generate_password_hash('secret', 10)
            bcrypt.check_password_hash(pw_hash, 'secret') # returns True

        :param pw_hash: The hash to be compared against.
        :param password: The password to compare.
        :return:
        """

        # Python 3 unicode strings must be encoded as bytes before hashing.
        pw_hash = self._unicode_to_bytes(pw_hash)
        password = self._unicode_to_bytes(password)

        if self._handle_long_passwords:
            password = hashlib.sha256(password).hexdigest()
            password = self._unicode_to_bytes(password)

        return safe_str_cmp(bcrypt.hashpw(password, pw_hash), pw_hash)
