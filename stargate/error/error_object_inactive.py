from stargate.helper import http_code


# Error handler
class ObjectInactiveError(Exception):
    """
        This is for object inactive error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'info'
        self.status_code = http_code.HTTP_403_FORBIDDEN
