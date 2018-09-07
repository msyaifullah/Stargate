from stargate.helper import http_code


# Error handler
class ResourceUnavailableError(Exception):
    """
        This is for resource unavailable error
    """

    def __init__(self, error):
        self.error = error
        self.severity = 'info'
        self.status_code = http_code.HTTP_500_INTERNAL_SERVER_ERROR
