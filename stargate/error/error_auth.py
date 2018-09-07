from stargate.helper import http_code


# Error handler
class AuthError(Exception):
    """
        This is for authentication error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'info'
        self.status_code = http_code.HTTP_403_FORBIDDEN
