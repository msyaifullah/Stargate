from stargate.helper.b_crypt import BCrypt


class Authentication(object):
    id = None
    name = None
    email = None
    phone = None
    fcm = None
    password_hash = None

    # New instance instantiation procedure
    def __init__(self, id=None, name=None, email=None, phone=None, fcm=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.fcm = fcm

    def set_password(self, password, secret):
        self.password_hash = BCrypt().generate_password_hash(password, secret).decode()
        return self.password_hash

    def is_password(self, hash, password):
        return BCrypt().check_password_hash(pw_hash=hash, password=password)

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

    def send_email(self, message):
        """

        :param message:
        :return:
        """
        pass

    def send_sms(self, message):
        """

        :param message:
        :return:
        """
        message = 'This is your secret code : \"{verification_code}\"'.format(verification_code=message)
        pass

    def send_fcm(self, message):
        """

        :param message:
        :return:
        """
        pass


class BlacklistToken(object):

    def __init__(self):
        pass

    @staticmethod
    def check_blacklist(auth_token):
        return False
