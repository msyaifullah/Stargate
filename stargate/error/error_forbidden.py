from stargate.helper import http_code


# Error handler
class ForbiddenError(Exception):
    """
        This is for forbidden error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'warning'
        self.status_code = http_code.HTTP_403_FORBIDDEN
