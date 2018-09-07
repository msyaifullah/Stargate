from stargate.helper import http_code


# Error handler
class ObjectNotFoundError(Exception):
    """
        This is for object not found error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'info'
        self.status_code = http_code.HTTP_404_NOT_FOUND
