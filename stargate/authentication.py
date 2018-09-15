import re

from pbkdf2 import crypt
from abc import abstractmethod


class Authentication(object):
    """
    You need to overide this class and and register it as
    """
    id = None
    name = None
    email = None
    phone = None
    fcm = None
    password_hash = None

    # New instance instantiation procedure
    def __init__(self, id=None, name=None, email=None, phone=None, fcm=None):
        """

        :param id:
        :param name:
        :param email:
        :param phone:
        :param fcm:
        """
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.fcm = fcm

    def set_password(self, password, secret):
        """

        :param password:
        :param secret:
        :return:
        """
        self.password_hash = crypt(word=password, salt=secret)
        return self.password_hash

    def is_password(self, username, password, secret):
        """

        :param username:
        :param password:
        :param secret:
        :return:
        """
        utype = self.username_type(username)
        uhash = self.get_hash_by_username(username, utype)
        if uhash is None or uhash is '':
            return False

        return self.is_hash_valid(uhash, password, secret)

    def is_hash_valid(self, uhash, password, secret):
        """

        :param password:
        :param uhash:
        :param secret:
        :return:
        """

        return (uhash == crypt(password, secret))

    def username_type(self, username):
        """

        :param username:
        :return:
        """
        if self.is_email(username):
            return 'email'
        elif self.is_phone(username):
            return 'phone'
        else:
            return None

    def is_email(self, username):
        """
        To check is username is email
        :param username:
        :return:
        """
        if len(username) > 7:
            pattern = re.compile(r"^(?!\.)(\"\"([^\"\"\r\\]|\\[\"\"\r\\])*\"\"|([-a-z0-9!#$%&'*+/=?^_`{|}~]|(?<!\.)\.)*)"
                                 r"(?<!\.)@[a-z0-9][\w\.-]*[a-z0-9]\.[a-z][a-z\.]*[a-z]$")
            return bool(pattern.match(username))
        else:
            return False

    def is_phone(self, username):
        """
        To check is username is phone number
        :param username:
        :return:
        """
        pattern = re.compile(
            r"^\(?(?P<prefix>(?=1)|\+|(?:0(?:0(?:0|1|9)?|1(?:0|1))?|119))[-. ]?\(?(?P<CC>1([-. ]?)"
            r"[0-9]{3}|2(?:0|[0-9]{2})|3(?:[0-469]|[0-9]{2})|4(?:[013-9]|[0-9]{2})|5(?:[1-8]|[0-9]"
            r"{2})|6(?:[0-6]|[0-9]{2})|7(?:[-. ]?[67]|[0-9]{3})|8(?:[1246]|[0-9]{2})|9(?:[0-58]|[0-9]"
            r"{2}))(?:\)?[-. ])?(?P<number>(?:[0-9]+[-. ]?)+)$")
        return bool(pattern.match(username))

    def send_notification(self, auth_verify_code):
        """

        :param auth_verify_code:
        :return:
        """

        carrier_type = None
        if self.fcm is not None:
            self.send_fcm(auth_verify_code)
            carrier_type = 'fcm'
        elif self.email is not None:
            self.send_email(auth_verify_code)
            carrier_type = 'email'
        elif self.phone is not None:
            self.send_sms(auth_verify_code)
            carrier_type = 'phone'

        return carrier_type

    @abstractmethod
    def send_email(self, message):
        """

        :param message:
        :return:
        """
        pass

    @abstractmethod
    def send_sms(self, message):
        """

        :param message:
        :return:
        """
        message = 'This is your secret code : \"{verification_code}\"'.format(verification_code=message)
        pass

    @abstractmethod
    def send_fcm(self, message):
        """

        :param message:
        :return:
        """
        pass

    @abstractmethod
    def get_hash_by_username(self, username, utype):
        """

        :param username: PhoneNumber | Email
        :param utype: 'phone'| 'email'
        :return:
        """
        pass

    @abstractmethod
    def is_refresh_token(self, token):
        """

        :param token:
        :return:
        """
        pass

    @abstractmethod
    def save_refresh_token(self, token, exp):
        """

        :param token:
        :param exp:
        :return:
        """
        pass

    @abstractmethod
    def remove_refresh_token(self, token):
        """

        :param token:
        :return:
        """
        pass
