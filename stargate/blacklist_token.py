from abc import abstractmethod


class BlacklistToken(object):

    def __init__(self):
        pass

    @abstractmethod
    def is_blacklisted(self, token):
        return False

    @abstractmethod
    def add_blacklist(self, token, exp):
        return True

    @abstractmethod
    def remove_blacklist(self, token):
        return True
