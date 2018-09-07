from stargate.helper import http_code


# Error handler
class VerificationError(Exception):
    """
        This is for user inactive error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'info'
        self.status_code = http_code.HTTP_401_UNAUTHORIZED
