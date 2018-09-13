from stargate.blacklist_token import BlacklistToken


class MyBlaclist(BlacklistToken):

    def is_blacklisted(self, token):
        print("is blacklisted")
        return False

    def add_blacklist(self, token, exp):
        print("added success")
        return True

    def remove_blacklist(self, token):
        print("token removed")
        return True
