from stargate.helper import http_code


# Error handler
class ServerAuthError(Exception):
    """
        This is for server auth error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'warning'
        self.status_code = http_code.HTTP_500_INTERNAL_SERVER_ERROR
