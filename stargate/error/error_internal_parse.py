from stargate.helper import http_code


# Error handler
class InternalParseError(Exception):
    """
        This is for internal parse error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'error'
        self.status_code = http_code.HTTP_500_INTERNAL_SERVER_ERROR
