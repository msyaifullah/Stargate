from stargate.helper import http_code


# Error handler
class InvalidHeaderError(Exception):
    """
        This is for invalid header error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'info'
        self.status_code = http_code.HTTP_400_BAD_REQUEST
