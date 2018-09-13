from stargate.authentication import Authentication


class MyAuthentication(Authentication):

    def send_email(self, message):
        print("will send email with the message ")
        print(message)

    def send_sms(self, message):
        print("will send sms with the message ")
        print(message)

    def send_fcm(self, message):
        print("will send fcm with the message ")
        print(message)

    def get_hash_by_username(self, username, utype):
        print("will send email with the message ")
        return "mmmmmmm"

    def is_password(self, username, password, secret):
        return True
